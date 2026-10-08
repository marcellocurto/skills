#!/usr/bin/env python3
"""Flag open review threads on code added after the pull request's first review.

Run it from a checkout of the pull request's head. A flagged thread sits on lines that review
rounds added, so its finding may come from an earlier fix rather than from the change as opened.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from fetch_review_context import ensure_authenticated, fetch_all, graphql, resolve_pr

FIRST_REVIEW_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      headRefOid baseRefOid
      reviews(first: 1) { nodes { commit { oid } } }
    }
  }
}
"""


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def git_output(cwd: Path, *args: str) -> str:
    completed = git(cwd, *args)
    if completed.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout


def is_ancestor(cwd: Path, commit: str, of: str) -> bool:
    completed = git(cwd, "merge-base", "--is-ancestor", commit, of)
    if completed.returncode not in (0, 1):
        raise RuntimeError(f"Could not compare {commit} with {of}: {completed.stderr.strip()}")
    return completed.returncode == 0


def blamed_commits(cwd: Path, path: str, start: int, end: int) -> list[str]:
    """Commits that last changed the lines at HEAD. `-C` follows lines moved or copied between files,
    so moving code during review keeps the commit that wrote it."""
    porcelain = git_output(cwd, "blame", "--porcelain", "-C", "-L", f"{start},{end}", "HEAD", "--", path)
    commits: list[str] = []
    for line in porcelain.splitlines():
        sha = line.split(" ", 1)[0]
        if len(sha) == 40 and all(char in "0123456789abcdef" for char in sha) and sha not in commits:
            commits.append(sha)
    return commits


def flag_thread(thread: dict[str, Any], first_reviewed: str, base: str, cwd: Path) -> dict[str, Any]:
    """Report whether a thread's lines were added after `first_reviewed`, ignoring code merged in from `base`.

    `added_after_first_review` is None when the thread has no line on the head side, such as an
    outdated thread or one on deleted lines.
    """
    end = thread.get("line")
    start = thread.get("startLine") or end
    flagged: dict[str, Any] = {
        "url": thread["comments"]["nodes"][0]["url"],
        "path": thread["path"],
        "lines": [start, end] if end else None,
        "added_after_first_review": None,
        "commits": [],
    }
    if end is None or thread.get("diffSide") != "RIGHT":
        return flagged
    added = [
        commit for commit in blamed_commits(cwd, thread["path"], start, end)
        if not is_ancestor(cwd, commit, first_reviewed) and not is_ancestor(cwd, commit, base)
    ]
    return {**flagged, "added_after_first_review": bool(added), "commits": added}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Repository in [HOST/]OWNER/REPO form")
    parser.add_argument("--pr", help="Pull-request number or URL; defaults to the current branch PR")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    cwd = Path.cwd()
    try:
        target = resolve_pr(args.repo, args.pr)
        ensure_authenticated(target.host)
        status = graphql(target.host, FIRST_REVIEW_QUERY, owner=target.owner, repo=target.repo,
                         number=target.number)["data"]["repository"]["pullRequest"]
        head = git_output(cwd, "rev-parse", "HEAD").strip()
        if head != status["headRefOid"]:
            raise RuntimeError(f"Check out the pull request's head {status['headRefOid'][:9]} first; HEAD is {head[:9]}")
        reviews = status["reviews"]["nodes"]
        threads = [thread for thread in fetch_all(target)["review_threads"] if not thread["isResolved"]]
        if not reviews or not threads:
            print(json.dumps({"first_reviewed_commit": None, "threads": []}, indent=2))
            return 0
        first_reviewed = reviews[0]["commit"]["oid"]
        for commit in (first_reviewed, status["baseRefOid"]):
            if git(cwd, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
                raise RuntimeError(f"Commit {commit[:9]} is not in this checkout; fetch it first")
        print(json.dumps({
            "first_reviewed_commit": first_reviewed,
            "threads": [flag_thread(thread, first_reviewed, status["baseRefOid"], cwd) for thread in threads],
        }, indent=2))
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
