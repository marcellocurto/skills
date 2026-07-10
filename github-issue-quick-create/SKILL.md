---
name: github-issue-quick-create
description: Draft and create one GitHub issue with minimal metadata using `gh` after explicit approval. Use for a simple bug, task, chore, or feature.
---

# GitHub Issue Quick Create

Draft one straightforward issue, then create the approved draft with `gh`.

## Scope

Handle exactly one simple bug, task, chore, or feature. Switch to `github-issue-create` for issue sets, PRDs, specs, implementation breakdowns, relationships, label creation, duplicate investigation, or detailed planning.

## Draft

1. Resolve the repository from the request or current repo when possible. Do not require `gh` or authentication when the user's context is enough to draft.
2. Inspect code only when a referenced file, function, failure, or repository behavior is needed to make the issue usable.
3. Ask only for a missing essential:
   - target repository when it cannot be resolved
   - expected outcome when the request cannot be titled or verified
   - expected and actual behavior for an otherwise unusable bug report
   - one observable completion criterion for an otherwise unusable task or feature
4. Use only explicit labels and assignees. Do not infer other metadata or create labels.

Use a compact body with `Summary` and `Acceptance Criteria`. For bugs with known reproduction details, add `Reproduction`, `Expected`, and `Actual`. Preserve user-provided implementation details under `Notes` or `Implementation plan`; do not add a generic file inventory.

Show the repository, title, exact body, and explicit labels or assignees. Do not wrap the draft in a code fence. End with: Reply "create" to create this issue, or tell me what to change.

## Publish

Create only after explicit approval. Before publishing, preflight `gh`, authentication, and the target repository. If preflight fails, keep the approved draft intact and report the missing prerequisite.

Pass the exact approved body to `gh issue create --title "<title>" --body-file -` on standard input. Add `--repo`, `--assignee`, and repeated `--label` only when explicit and approved. Do not silently drop or replace invalid metadata after a failed command.

## Output

Return `#N - title - URL`, followed by any explicit labels or assignees that were successfully applied.

## Stop Rules

Stop after showing the draft and wait for approval. After publishing, stop when the issue number, title, and URL are reported. Ask only when a missing essential prevents a usable draft.
