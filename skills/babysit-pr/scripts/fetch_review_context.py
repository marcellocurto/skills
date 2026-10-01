#!/usr/bin/env python3
"""Fetch complete pull-request review context through the GitHub CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

PR_PATH = re.compile(r"^/([^/]+)/([^/]+)/pull/([1-9]\d*)(?:/.*)?$")


@dataclass(frozen=True)
class PullRequestTarget:
    host: str
    owner: str
    repo: str
    number: int

CONVERSATION_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number url title state baseRefName headRefName
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { id url body createdAt updatedAt author { login } }
      }
    }
  }
}
"""

REVIEWS_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number url title state baseRefName headRefName
      reviews(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { id url state body submittedAt author { login } }
      }
    }
  }
}
"""

THREADS_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number url title state baseRefName headRefName
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line diffSide startLine startDiffSide
          originalLine originalStartLine resolvedBy { login }
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id url body diffHunk createdAt updatedAt author { login }
            }
          }
        }
      }
    }
  }
}
"""

THREAD_COMMENTS_QUERY = """\
query($thread_id: ID!, $cursor: String!) {
  node(id: $thread_id) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id url body diffHunk createdAt updatedAt author { login }
        }
      }
    }
  }
}
"""


def run(command: list[str], stdin: str | None = None) -> str:
    completed = subprocess.run(command, input=stdin, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}")
    return completed.stdout


def run_json(command: list[str], stdin: str | None = None) -> dict[str, Any]:
    output = run(command, stdin=stdin)
    try:
        payload = json.loads(output)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"GitHub CLI returned invalid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise RuntimeError("GitHub CLI returned an unexpected JSON value")
    return payload


def ensure_authenticated(host: str) -> None:
    try:
        run(["gh", "auth", "status", "--active", "--hostname", host])
    except (FileNotFoundError, RuntimeError) as error:
        raise RuntimeError(
            f"Could not verify the active GitHub account on {host}: {error}\n"
            f"If authentication needs repair, run `gh auth login --hostname {host}`."
        ) from error


def parse_pr_url(url: str) -> PullRequestTarget:
    parsed = urlsplit(url)
    match = PR_PATH.fullmatch(parsed.path)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or not match:
        raise ValueError(f"Unsupported pull-request URL: {url}")
    owner, repo, number = match.groups()
    return PullRequestTarget(parsed.netloc.lower(), owner, repo, int(number))


def parse_repository(value: str, default_host: str | None = None) -> tuple[str, str, str]:
    parts = value.split("/")
    if len(parts) == 2 and all(parts):
        return default_host or os.environ.get("GH_HOST") or "github.com", *parts
    if len(parts) == 3 and all(parts):
        return parts[0].lower(), parts[1], parts[2]
    raise ValueError("--repo must be [HOST/]OWNER/REPO")


def resolve_pr(repo: str | None, pr: str | None) -> PullRequestTarget:
    if pr and "://" in pr:
        target = parse_pr_url(pr)
        if repo and tuple(part.lower() for part in parse_repository(repo, target.host)) != (
            target.host, target.owner.lower(), target.repo.lower()
        ):
            raise ValueError("--repo does not match the repository in --pr")
        return target

    if pr:
        if not pr.isdigit() or int(pr) < 1:
            raise ValueError("--pr must be a pull-request number or GitHub pull-request URL")
        if not repo:
            repository = run_json(["gh", "repo", "view", "--json", "url"])
            return parse_pr_url(f"{str(repository['url']).rstrip('/')}/pull/{pr}")
        host, owner, name = parse_repository(repo)
        return PullRequestTarget(host, owner, name, int(pr))

    if repo:
        raise ValueError("--repo requires --pr")

    current = run_json(["gh", "pr", "view", "--json", "number,url"])
    return parse_pr_url(str(current["url"]))


def graphql(host: str, query: str, **variables: str | int | None) -> dict[str, Any]:
    command = [
        "gh",
        "api",
        "graphql",
        "--hostname",
        host,
        "-F",
        "query=@-",
    ]
    for name, value in variables.items():
        if value is not None:
            command.extend(["-F", f"{name}={value}"])
    payload = run_json(command, stdin=query)
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors: {json.dumps(payload['errors'])}")
    return payload


def next_cursor(connection: dict[str, Any]) -> str | None:
    page_info = connection["pageInfo"]
    if not page_info["hasNextPage"]:
        return None
    cursor = page_info["endCursor"]
    if not cursor:
        raise RuntimeError("GitHub reported more results without a pagination cursor")
    return str(cursor)


def fetch_connection(
    query: str, connection_name: str, target: PullRequestTarget
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    cursor: str | None = None
    metadata: dict[str, Any] | None = None
    nodes: list[dict[str, Any]] = []

    while True:
        payload = graphql(
            target.host, query,
            owner=target.owner, repo=target.repo, number=target.number, cursor=cursor,
        )
        repository = payload.get("data", {}).get("repository")
        pull_request = repository and repository.get("pullRequest")
        if not pull_request:
            raise RuntimeError(f"Pull request {target.host}/{target.owner}/{target.repo}#{target.number} was not found")

        if metadata is None:
            metadata = {
                "host": target.host,
                "owner": target.owner,
                "repo": target.repo,
                "number": pull_request["number"],
                "url": pull_request["url"],
                "title": pull_request["title"],
                "state": pull_request["state"],
                "base_ref": pull_request["baseRefName"],
                "head_ref": pull_request["headRefName"],
            }

        connection = pull_request[connection_name]
        nodes.extend(connection.get("nodes") or [])
        cursor = next_cursor(connection)
        if cursor is None:
            break

    assert metadata is not None
    return metadata, nodes


def complete_thread_comments(host: str, thread: dict[str, Any]) -> None:
    comments = thread["comments"]
    cursor = next_cursor(comments)
    while cursor is not None:
        payload = graphql(host, THREAD_COMMENTS_QUERY, thread_id=thread["id"], cursor=cursor)
        node = payload.get("data", {}).get("node")
        if not node or "comments" not in node:
            raise RuntimeError(f"Could not fetch the remaining comments for thread {thread['id']}")
        page = node["comments"]
        comments["nodes"].extend(page["nodes"])
        comments["pageInfo"] = page["pageInfo"]
        following_cursor = next_cursor(page)
        if following_cursor == cursor:
            raise RuntimeError(f"Comment pagination did not advance for thread {thread['id']}")
        cursor = following_cursor


def fetch_all(target: PullRequestTarget) -> dict[str, Any]:
    metadata, conversation_comments = fetch_connection(
        CONVERSATION_QUERY, "comments", target
    )
    _, reviews = fetch_connection(REVIEWS_QUERY, "reviews", target)
    _, review_threads = fetch_connection(THREADS_QUERY, "reviewThreads", target)
    for thread in review_threads:
        complete_thread_comments(target.host, thread)
    return {
        "pull_request": metadata,
        "conversation_comments": conversation_comments,
        "reviews": reviews,
        "review_threads": review_threads,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Repository in [HOST/]OWNER/REPO form")
    parser.add_argument("--pr", help="Pull-request number or URL; defaults to the current branch PR")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        target = resolve_pr(args.repo, args.pr)
        ensure_authenticated(target.host)
        print(json.dumps(fetch_all(target), indent=2))
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
