#!/usr/bin/env python3
"""Create and verify one native GitHub issue relationship through `gh api`."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any


def run(command: list[str]) -> str:
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}")
    return completed.stdout


def parse_repository(value: str) -> tuple[str, str]:
    parts = value.split("/")
    if len(parts) == 2 and all(parts):
        return os.environ.get("GH_HOST") or "github.com", value
    if len(parts) == 3 and all(parts):
        return parts[0], "/".join(parts[1:])
    raise ValueError("--repo must be [HOST/]OWNER/REPO")


def api_json(host: str, command: list[str]) -> Any:
    output = run(["gh", "api", "--hostname", host, *command])
    try:
        return json.loads(output)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"GitHub CLI returned invalid JSON: {error}") from error


def issue(host: str, repo: str, number: int) -> dict[str, Any]:
    payload = api_json(host, [f"repos/{repo}/issues/{number}"])
    if not isinstance(payload, dict):
        raise RuntimeError(f"GitHub returned an unexpected issue payload for #{number}")
    return payload


def relationship_ids(host: str, endpoint: str) -> set[int]:
    pages = api_json(
        host,
        [endpoint, "-f", "per_page=100", "--method", "GET", "--paginate", "--slurp"],
    )
    if not isinstance(pages, list) or not all(isinstance(page, list) for page in pages):
        raise RuntimeError("GitHub returned an unexpected relationship payload")
    return {int(item["id"]) for page in pages for item in page}


def add_sub_issue(host: str, repo: str, parent: int, child: int) -> dict[str, Any]:
    endpoint = f"repos/{repo}/issues/{parent}/sub_issues"
    child_id = int(issue(host, repo, child)["id"])
    if child_id in relationship_ids(host, endpoint):
        return {
            "relationship": "sub-issue",
            "parent": parent,
            "child": child,
            "created": False,
            "verified": True,
        }
    api_json(
        host,
        [
            "--method",
            "POST",
            f"repos/{repo}/issues/{parent}/sub_issues",
            "-F",
            f"sub_issue_id={child_id}",
        ]
    )
    if child_id not in relationship_ids(host, endpoint):
        raise RuntimeError(f"GitHub did not report #{child} as a sub-issue of #{parent}")
    return {
        "relationship": "sub-issue",
        "parent": parent,
        "child": child,
        "created": True,
        "verified": True,
    }


def add_blocker(host: str, repo: str, blocked: int, blocker: int) -> dict[str, Any]:
    endpoint = f"repos/{repo}/issues/{blocked}/dependencies/blocked_by"
    blocker_id = int(issue(host, repo, blocker)["id"])
    if blocker_id in relationship_ids(host, endpoint):
        return {
            "relationship": "blocked-by",
            "blocked": blocked,
            "blocker": blocker,
            "created": False,
            "verified": True,
        }
    api_json(
        host,
        [
            "--method",
            "POST",
            f"repos/{repo}/issues/{blocked}/dependencies/blocked_by",
            "-F",
            f"issue_id={blocker_id}",
        ]
    )
    if blocker_id not in relationship_ids(host, endpoint):
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
    parser.add_argument("--repo", required=True, help="Repository in [HOST/]OWNER/REPO form")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--parent", type=int, help="Parent issue number")
    mode.add_argument("--blocked", type=int, help="Blocked issue number")
    parser.add_argument("--sub-issue", type=int, help="Sub-issue number used with --parent")
    parser.add_argument("--blocked-by", type=int, help="Blocking issue number used with --blocked")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        host, repo = parse_repository(args.repo)
        if args.parent is not None:
            if args.sub_issue is None or args.blocked_by is not None:
                raise ValueError("--parent requires --sub-issue and cannot use --blocked-by")
        else:
            if args.blocked_by is None or args.sub_issue is not None:
                raise ValueError("--blocked requires --blocked-by and cannot use --sub-issue")
        run(["gh", "auth", "status", "--active", "--hostname", host])
        if args.parent is not None:
            result = add_sub_issue(host, repo, args.parent, args.sub_issue)
        else:
            result = add_blocker(host, repo, args.blocked, args.blocked_by)
        result["repository"] = f"{host}/{repo}"
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
