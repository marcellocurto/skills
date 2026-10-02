#!/usr/bin/env python3
"""Poll a pull request until Codex finishes reviewing its head and someone needs an answer."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any

from fetch_review_context import PullRequestTarget, ensure_authenticated, fetch_all, graphql, resolve_pr

CODEX_LOGIN = "chatgpt-codex-connector"
SUMMARY_MARKER = "<!-- codex-pull-request-review-summary -->"
# A summary table row: | 📝 **Code Review** | ✅ **Completed** <relative-time …> | `b5568c0` | New commits |
SUMMARY_ROW = re.compile(r"^\|\s*(?P<review>[^|]+?)\s*\|\s*(?P<status>[^|]+?)\s*\|\s*`(?P<commit>[0-9a-f]{7,40})`\s*\|")

STATUS_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!) {
  viewer { login }
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      headRefOid
      commits(last: 1) { nodes { commit { committedDate } } }
      reactions(first: 100) { nodes { content createdAt user { login } } }
      reviews(last: 100) { nodes { author { login } submittedAt commit { oid } } }
    }
  }
}
"""


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def is_codex(actor: dict[str, Any] | None) -> bool:
    return bool(actor) and str(actor["login"]).removesuffix("[bot]") == CODEX_LOGIN


def is_summary(comment: dict[str, Any]) -> bool:
    return is_codex(comment.get("author")) and SUMMARY_MARKER in (comment.get("body") or "")


def summary_rows(conversation_comments: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Read Codex's self-updating summary table: one row per review kind, naming the commit it last covered."""
    summary = next((comment for comment in conversation_comments if is_summary(comment)), None)
    if summary is None:
        return []
    rows = []
    for line in summary["body"].splitlines():
        match = SUMMARY_ROW.match(line.strip())
        if not match:
            continue
        status = match["status"]
        rows.append({
            "review": match["review"].replace("*", "").strip(),
            "status": "running" if "Running" in status or "Queued" in status
            else "completed" if "Completed" in status
            else re.sub(r"<[^>]*>|\*", "", status).strip(),
            "commit": match["commit"],
        })
    return rows


def codex_review(pull_request: dict[str, Any], conversation_comments: list[dict[str, Any]]) -> dict[str, Any]:
    """Classify Codex's review of the head commit as running, pending, failed, findings, or approved.

    Codex reacts with 👀 while any review runs, posts a review tagged with the commit when it has
    suggestions, and reacts with 👍 when all reviews finish clean. The 👍 is not tied to a commit and
    can survive later pushes, so approval also requires every summary row to cover the head commit.

    A review with findings on the head commit is superseded by a 👍 posted after it, which is how a
    clean re-review of the same commit (after the findings were answered without a push) shows up.

    Without a summary table the 👍 must postdate the head commit's recorded date. GitHub does not
    expose when a commit was pushed, so a commit with an old date pushed after an old 👍 cannot be
    told apart from an approved head in that fallback.
    """
    head = pull_request["headRefOid"]
    rows = summary_rows(conversation_comments)
    head_rows = [row for row in rows if head.startswith(row["commit"])]
    reactions = {
        reaction["content"]: reaction
        for reaction in pull_request["reactions"]["nodes"]
        if is_codex(reaction.get("user"))
    }
    codex_reviews = [review for review in pull_request["reviews"]["nodes"] if is_codex(review.get("author"))]
    latest_review_at = max((parse_time(review["submittedAt"]) for review in codex_reviews), default=None)
    latest_head_review_at = max(
        (parse_time(review["submittedAt"]) for review in codex_reviews
         if (review.get("commit") or {}).get("oid") == head),
        default=None,
    )
    thumbs_up = reactions.get("THUMBS_UP")
    thumbs_up_at = parse_time(thumbs_up["createdAt"]) if thumbs_up else None

    if "EYES" in reactions or any(row["status"] == "running" for row in head_rows):
        state = "running"
    elif len(head_rows) < len(rows):
        state = "pending"
    elif any(row["status"] != "completed" for row in head_rows):
        state = "failed"
    elif latest_head_review_at and not (thumbs_up_at and thumbs_up_at > latest_head_review_at):
        state = "findings"
    elif thumbs_up and rows:
        state = "approved"
    elif thumbs_up_at and thumbs_up_at > head_commit_time(pull_request) and not (
        latest_review_at and thumbs_up_at < latest_review_at
    ):
        # Without a summary table, only a 👍 newer than the head commit and newer than Codex's
        # last review of any commit can be about the head.
        state = "approved"
    else:
        state = "pending"
    return {"state": state, "reviews": rows}


def head_commit_time(pull_request: dict[str, Any]) -> datetime:
    return parse_time(pull_request["commits"]["nodes"][-1]["commit"]["committedDate"])


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
        if not is_summary(comment):
            add("comment", comment, comment.get("createdAt"))
    for review in context["reviews"]:
        # A bodiless COMMENTED review only wraps inline comments, which are listed on their own.
        if review.get("body") or review.get("state") != "COMMENTED":
            add("review", review, review.get("submittedAt"))
    for thread in context["review_threads"]:
        for comment in thread["comments"]["nodes"]:
            add("thread-comment", comment, comment.get("createdAt"))
    return items


def check(target: PullRequestTarget, since: datetime | None) -> dict[str, Any]:
    # Taken before fetching, so the next `--since` cannot skip a comment posted mid-fetch.
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    context = fetch_all(target)
    status = graphql(target.host, STATUS_QUERY, owner=target.owner, repo=target.repo, number=target.number)
    pull_request = status["data"]["repository"]["pullRequest"]
    metadata = context["pull_request"]
    return {
        "pull_request": {
            "url": metadata["url"],
            "state": metadata["state"],
            "head_sha": pull_request["headRefOid"],
        },
        "checked_at": checked_at,
        "codex": codex_review(pull_request, context["conversation_comments"]),
        "new_activity": new_activity(context, status["data"]["viewer"]["login"], since),
        "unresolved_threads": sum(not thread["isResolved"] for thread in context["review_threads"]),
    }


def wake_reason(snapshot: dict[str, Any]) -> str | None:
    if snapshot["pull_request"]["state"] != "OPEN":
        return "closed"
    codex_state = snapshot["codex"]["state"]
    # Feedback that arrives mid-review is answered together with Codex's findings in one push.
    if codex_state == "running":
        return None
    if snapshot["new_activity"]:
        return "new-activity"
    return {"approved": "codex-approved", "failed": "codex-failed"}.get(codex_state)


def watch(target: PullRequestTarget, since: datetime | None, interval: float, timeout: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while True:
        snapshot = check(target, since)
        reason = wake_reason(snapshot)
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
