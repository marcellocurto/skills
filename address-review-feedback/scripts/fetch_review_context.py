#!/usr/bin/env python3
"""Fetch complete pull-request review context through the GitHub CLI."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any

PR_URL = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/pull/(\d+)(?:/.*)?$")

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


def ensure_authenticated() -> None:
    try:
        run(["gh", "auth", "status"])
    except (FileNotFoundError, RuntimeError) as error:
        raise RuntimeError(
            "GitHub CLI authentication is required; install `gh` if needed and run `gh auth login`"
        ) from error


def parse_pr_url(url: str) -> tuple[str, str, int]:
    match = PR_URL.match(url)
    if not match:
        raise ValueError(f"Unsupported pull-request URL: {url}")
    owner, repo, number = match.groups()
    return owner, repo, int(number)


def resolve_pr(repo: str | None, pr: str | None) -> tuple[str, str, int]:
    if pr and PR_URL.match(pr):
        owner, name, number = parse_pr_url(pr)
        if repo and repo != f"{owner}/{name}":
            raise ValueError("--repo does not match the repository in --pr")
        return owner, name, number

    if pr:
        if not pr.isdigit():
            raise ValueError("--pr must be a pull-request number or GitHub pull-request URL")
        if not repo:
            repository = run_json(["gh", "repo", "view", "--json", "nameWithOwner"])
            repo = str(repository["nameWithOwner"])
        owner, name = repo.split("/", 1)
        return owner, name, int(pr)

    if repo:
        raise ValueError("--repo requires --pr")

    current = run_json(["gh", "pr", "view", "--json", "number,url"])
    return parse_pr_url(str(current["url"]))


def graphql(
    query: str, owner: str, repo: str, number: int, cursor: str | None
) -> dict[str, Any]:
    command = [
        "gh",
        "api",
        "graphql",
        "-F",
        "query=@-",
        "-F",
        f"owner={owner}",
        "-F",
        f"repo={repo}",
        "-F",
        f"number={number}",
    ]
    if cursor:
        command.extend(["-F", f"cursor={cursor}"])
    payload = run_json(command, stdin=query)
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors: {json.dumps(payload['errors'])}")
    return payload


def fetch_connection(
    query: str, connection_name: str, owner: str, repo: str, number: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    cursor: str | None = None
    metadata: dict[str, Any] | None = None
    nodes: list[dict[str, Any]] = []

    while True:
        payload = graphql(query, owner, repo, number, cursor)
        repository = payload.get("data", {}).get("repository")
        pull_request = repository and repository.get("pullRequest")
        if not pull_request:
            raise RuntimeError(f"Pull request {owner}/{repo}#{number} was not found")

        if metadata is None:
            metadata = {
                "owner": owner,
                "repo": repo,
                "number": pull_request["number"],
                "url": pull_request["url"],
                "title": pull_request["title"],
                "state": pull_request["state"],
                "base_ref": pull_request["baseRefName"],
                "head_ref": pull_request["headRefName"],
            }

        connection = pull_request[connection_name]
        nodes.extend(connection.get("nodes") or [])
        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    assert metadata is not None
    return metadata, nodes


def fetch_all(owner: str, repo: str, number: int) -> dict[str, Any]:
    metadata, conversation_comments = fetch_connection(
        CONVERSATION_QUERY, "comments", owner, repo, number
    )
    _, reviews = fetch_connection(REVIEWS_QUERY, "reviews", owner, repo, number)
    _, review_threads = fetch_connection(THREADS_QUERY, "reviewThreads", owner, repo, number)
    return {
        "pull_request": metadata,
        "conversation_comments": conversation_comments,
        "reviews": reviews,
        "review_threads": review_threads,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Repository in OWNER/REPO form")
    parser.add_argument("--pr", help="Pull-request number or URL; defaults to the current branch PR")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        ensure_authenticated()
        owner, repo, number = resolve_pr(args.repo, args.pr)
        print(json.dumps(fetch_all(owner, repo, number), indent=2))
    except (KeyError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
