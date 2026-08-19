#!/usr/bin/env python3
"""Create and verify one native GitHub issue relationship through `gh api`."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any


def run(command: list[str]) -> str:
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}")
    return completed.stdout


def api_json(command: list[str]) -> Any:
    output = run(["gh", "api", *command])
    try:
        return json.loads(output)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"GitHub CLI returned invalid JSON: {error}") from error


def issue(repo: str, number: int) -> dict[str, Any]:
    payload = api_json([f"repos/{repo}/issues/{number}"])
    if not isinstance(payload, dict):
        raise RuntimeError(f"GitHub returned an unexpected issue payload for #{number}")
    return payload


def relationship_numbers(repo: str, endpoint: str) -> set[int]:
    payload = api_json([endpoint, "-f", "per_page=100", "--method", "GET"])
    if not isinstance(payload, list):
        raise RuntimeError("GitHub returned an unexpected relationship payload")
    return {int(item["number"]) for item in payload if isinstance(item, dict) and "number" in item}


def add_sub_issue(repo: str, parent: int, child: int) -> dict[str, Any]:
    endpoint = f"repos/{repo}/issues/{parent}/sub_issues"
    if child in relationship_numbers(repo, endpoint):
        return {
            "relationship": "sub-issue",
            "parent": parent,
            "child": child,
            "created": False,
            "verified": True,
        }
    child_id = int(issue(repo, child)["id"])
    api_json(
        [
            "--method",
            "POST",
            f"repos/{repo}/issues/{parent}/sub_issues",
            "-F",
            f"sub_issue_id={child_id}",
        ]
    )
    if child not in relationship_numbers(repo, endpoint):
        raise RuntimeError(f"GitHub did not report #{child} as a sub-issue of #{parent}")
    return {
        "relationship": "sub-issue",
        "parent": parent,
        "child": child,
        "created": True,
        "verified": True,
    }


def add_blocker(repo: str, blocked: int, blocker: int) -> dict[str, Any]:
    endpoint = f"repos/{repo}/issues/{blocked}/dependencies/blocked_by"
    if blocker in relationship_numbers(repo, endpoint):
        return {
            "relationship": "blocked-by",
            "blocked": blocked,
            "blocker": blocker,
            "created": False,
            "verified": True,
        }
    blocker_id = int(issue(repo, blocker)["id"])
    api_json(
        [
            "--method",
            "POST",
            f"repos/{repo}/issues/{blocked}/dependencies/blocked_by",
            "-F",
            f"issue_id={blocker_id}",
        ]
    )
    if blocker not in relationship_numbers(repo, endpoint):
        raise RuntimeError(f"GitHub did not report #{blocked} as blocked by #{blocker}")
    return {
        "relationship": "blocked-by",
        "blocked": blocked,
        "blocker": blocker,
        "created": True,
        "verified": True,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Repository in OWNER/REPO form")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--parent", type=int, help="Parent issue number")
    mode.add_argument("--blocked", type=int, help="Blocked issue number")
    parser.add_argument("--sub-issue", type=int, help="Sub-issue number used with --parent")
    parser.add_argument("--blocked-by", type=int, help="Blocking issue number used with --blocked")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        run(["gh", "auth", "status"])
        if args.parent is not None:
            if args.sub_issue is None or args.blocked_by is not None:
                raise ValueError("--parent requires --sub-issue and cannot use --blocked-by")
            result = add_sub_issue(args.repo, args.parent, args.sub_issue)
        else:
            if args.blocked_by is None or args.sub_issue is not None:
                raise ValueError("--blocked requires --blocked-by and cannot use --sub-issue")
            result = add_blocker(args.repo, args.blocked, args.blocked_by)
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
