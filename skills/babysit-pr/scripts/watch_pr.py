#!/usr/bin/env python3
"""Poll a pull request until someone needs an answer, a check finishes, or the PR conflicts with its base, and
report which commits this skill has reviewed."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from typing import Any

from fetch_review_context import PullRequestTarget, ensure_authenticated, fetch_all, graphql, next_cursor, resolve_pr

# Bodies of the reviews this skill posts, as `REVIEWERS.md` specifies them. Each is pinned to the
# commit it covers, so these prefixes plus the review's commit say what has been reviewed.
FIRST_REVIEW_PREFIX = "Reviewed `"
FIX_CHECK_PREFIX = "Reviewed the fixes in `"

STATUS_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  viewer { login }
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      headRefOid
      mergeable
      commits(last: 1) {
        nodes {
          commit {
            statusCheckRollup {
              contexts(first: 100, after: $cursor) {
                pageInfo { hasNextPage endCursor }
                nodes {
                  __typename
                  ... on CheckRun {
                    name status conclusion completedAt detailsUrl
                    isRequired(pullRequestNumber: $number)
                  }
                  ... on StatusContext {
                    context state createdAt targetUrl
                    isRequired(pullRequestNumber: $number)
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

# Check-run conclusions that pass; every other conclusion fails, as GitHub treats it for required checks.
PASSING_CONCLUSIONS = {"SUCCESS", "NEUTRAL", "SKIPPED"}
PENDING_STATUS_STATES = {"PENDING", "EXPECTED"}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def own_reviews(reviews: list[dict[str, Any]], viewer: str) -> dict[str, Any]:
    """Summarize the first reviews and fix checks the viewer posted, in submission order.

    `first_reviewed_commit` is the commit of the latest first review, which is the baseline for code
    added in review rounds; a rebase prompts a new first review, which replaces the baseline.
    `last_reviewed_commit` is the commit of the latest first review or fix check. Both are None when
    the pull request has no first review yet. `fix_checks` counts the fix checks, one per round that
    checked new commits.
    """
    own = [review for review in reviews
           if (review.get("author") or {}).get("login") == viewer and (review.get("commit") or {}).get("oid")]
    first_reviews = [review for review in own if (review.get("body") or "").startswith(FIRST_REVIEW_PREFIX)]
    reviewed = [review for review in own
                if (review.get("body") or "").startswith((FIRST_REVIEW_PREFIX, FIX_CHECK_PREFIX))]
    return {
        "first_reviewed_commit": first_reviews[-1]["commit"]["oid"] if first_reviews else None,
        "last_reviewed_commit": reviewed[-1]["commit"]["oid"] if first_reviews else None,
        "fix_checks": len(reviewed) - len(first_reviews),
    }


def new_activity(context: dict[str, Any], viewer: str, since: datetime | None) -> list[dict[str, str]]:
    """List comments and reviews from anyone but the viewer posted or edited after `since`."""
    items = []

    def add(kind: str, node: dict[str, Any], created_at: str | None) -> None:
        author = (node.get("author") or {}).get("login", "ghost")
        if author == viewer or not created_at:
            return
        # An edit counts as activity, so the item's time is its latest change.
        changed_at = max(created_at, node.get("updatedAt") or created_at, key=parse_time)
        # `since` is a whole-second floor, so an item from that same second is reported
        # again rather than skipped; a repeated round costs less than a missed comment.
        if since and parse_time(changed_at) < since:
            return
        items.append({"kind": kind, "author": author, "url": node.get("url", ""),
                      "created_at": created_at, "changed_at": changed_at})

    for comment in context["conversation_comments"]:
        add("comment", comment, comment.get("createdAt"))
    for review in context["reviews"]:
        # A bodiless COMMENTED review only wraps inline comments, which are listed on their own.
        if review.get("body") or review.get("state") != "COMMENTED":
            add("review", review, review.get("submittedAt"))
    for thread in context["review_threads"]:
        for comment in thread["comments"]["nodes"]:
            add("thread-comment", comment, comment.get("createdAt"))
    return items


def summarize_checks(contexts: list[dict[str, Any]]) -> dict[str, Any]:
    """List the head commit's failing and unfinished checks, from GitHub Actions or commit statuses.

    `last_completed_at` is when the latest check finished, so a watch can tell that checks finished
    after its `--since` even when they all passed.
    """
    failing, pending, completed = [], [], []
    for context in contexts:
        if context.get("__typename") == "CheckRun":
            name, url, required = context["name"], context.get("detailsUrl"), context.get("isRequired", False)
            finished = context["status"] == "COMPLETED"
            failed = finished and context.get("conclusion") not in PASSING_CONCLUSIONS
            completed_at = context.get("completedAt")
        else:
            name, url, required = context["context"], context.get("targetUrl"), context.get("isRequired", False)
            finished = context["state"] not in PENDING_STATUS_STATES
            failed = context["state"] in {"ERROR", "FAILURE"}
            completed_at = context.get("createdAt")
        entry = {"name": name, "required": required, "url": url}
        if not finished:
            pending.append(entry)
            continue
        if completed_at:
            completed.append(completed_at)
        if failed:
            failing.append({**entry, "completed_at": completed_at})
    return {
        "failing": failing,
        "pending": pending,
        "last_completed_at": max(completed, key=parse_time) if completed else None,
    }


def fetch_status(target: PullRequestTarget) -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
    """Return the pull request's head and mergeability, the viewer's login, and every check on the head."""
    cursor: str | None = None
    contexts: list[dict[str, Any]] = []
    while True:
        data = graphql(target.host, STATUS_QUERY, owner=target.owner, repo=target.repo,
                       number=target.number, cursor=cursor)["data"]
        pull_request = data["repository"]["pullRequest"]
        commits = pull_request["commits"]["nodes"]
        rollup = commits[0]["commit"]["statusCheckRollup"] if commits else None
        if rollup is None:
            return pull_request, data["viewer"]["login"], contexts
        contexts.extend(rollup["contexts"]["nodes"])
        cursor = next_cursor(rollup["contexts"])
        if cursor is None:
            return pull_request, data["viewer"]["login"], contexts


def check(target: PullRequestTarget, since: datetime | None) -> dict[str, Any]:
    # Taken before fetching, so the next `--since` cannot skip a comment posted mid-fetch.
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    context = fetch_all(target)
    pull_request, viewer, contexts = fetch_status(target)
    metadata = context["pull_request"]
    return {
        "pull_request": {
            "url": metadata["url"],
            "state": metadata["state"],
            "head_sha": pull_request["headRefOid"],
            # MERGEABLE, CONFLICTING, or UNKNOWN while GitHub is still computing it.
            "mergeable": pull_request["mergeable"],
        },
        "checked_at": checked_at,
        "reviews": own_reviews(context["reviews"], viewer),
        "checks": summarize_checks(contexts),
        "new_activity": new_activity(context, viewer, since),
        "unresolved_threads": sum(not thread["isResolved"] for thread in context["review_threads"]),
    }


def wake_reason(snapshot: dict[str, Any], since: datetime | None) -> str | None:
    def after_since(value: str | None) -> bool:
        # Same whole-second floor as `new_activity`: a repeat costs less than a missed result.
        return bool(value) and (since is None or parse_time(value) >= since)

    pull_request, checks = snapshot["pull_request"], snapshot["checks"]
    if pull_request["state"] != "OPEN":
        return "closed"
    if snapshot["new_activity"]:
        return "new-activity"
    if pull_request["mergeable"] == "CONFLICTING":
        return "conflict"
    if any(after_since(failed["completed_at"]) for failed in checks["failing"]):
        return "check-failed"
    if not checks["pending"] and after_since(checks["last_completed_at"]):
        return "checks-finished"
    return None


def watch(target: PullRequestTarget, since: datetime | None, interval: float, timeout: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while True:
        snapshot = check(target, since)
        reason = wake_reason(snapshot, since)
        if reason is None and time.monotonic() + interval > deadline:
            reason = "timeout"
        if reason:
            return {"reason": reason, **snapshot}
        time.sleep(interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Repository in [HOST/]OWNER/REPO form")
    parser.add_argument("--pr", help="Pull-request number or URL; defaults to the current branch PR")
    parser.add_argument("--since", type=parse_time, help="Only report activity after this ISO time, "
                        "normally the previous run's checked_at")
    parser.add_argument("--interval", type=float, default=2, help="Minutes between checks (default 2)")
    parser.add_argument("--timeout", type=float, default=30, help="Minutes to wait before giving up (default 30)")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        target = resolve_pr(args.repo, args.pr)
        ensure_authenticated(target.host)
        result = watch(target, args.since, args.interval * 60, args.timeout * 60)
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
