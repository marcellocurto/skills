---
name: create-pull-request
description: Open a ready-for-review GitHub pull request for completed local changes, including any needed commit and push.
---

# Create Pull Request

Publish one completed change as a clear, accurate, ready-for-review GitHub pull request.

A direct request to create, open, or publish the PR authorizes the ordinary commit, push, and PR creation needed for that exact change. If a matching open PR already exists, this includes updating its title and body to reflect the completed change and marking it ready for review. It does not authorize force-pushing, merging, issue edits, labels, reviewers, assignees, or unrelated local changes.

Leave the published PR open for review. Merging requires a separate explicit user instruction after publication and delivery of the PR URL, even if the original request bundled creation and merging. Do not merge, enable auto-merge, or enqueue a merge during this workflow.

## Establish the change

- Read the repository instructions for branches, commits, verification, and pull requests, including the applicable PR template.
- Resolve the exact GitHub host, base repository, head repository, and push remote from the user's request, repository instructions, and Git remotes. Ask when the intended destination remains ambiguous.
- Use the user's requested head branch, otherwise the current branch. Use the requested base branch; when unspecified, follow repository instructions, then `branch.<head>.gh-merge-base`, then GitHub's default branch. Ask if repository instructions and explicit branch configuration conflict. A default or protected branch can be the PR head; respect restrictions on the actual push operation.
- Do not create or switch branches by default. If publication requires creating or switching a branch, explain the concrete reason and proposed branch, ask for permission, and wait before proceeding unless the user has already explicitly authorized that action. A request to publish a PR alone is not permission to change branches. Resolve a detached HEAD or a head and base that identify the same branch under this rule.
- Record the resolved head ref and commit. Use them for the diff, verification, push, and PR comparison; local `HEAD` represents the requested head only when they match. When the intended commit is already the remote head, inspect that ref without requiring a checkout or push. Commit local changes only in a checkout of the selected head, subject to the branch permission rule.
- Inspect the complete merge-base diff from the fetched base to the selected head, its commits, and any local changes intended for publication, including staged and unstaged changes, untracked files, and `git diff --check`.
- Preserve unrelated worktree changes. Stage only clearly in-scope paths; never stash, discard, clean, reset, amend, rebase, or rewrite history merely to publish the PR.
- Check for an existing open PR with the same base repository and branch and head repository and branch. Read its title, body, and draft state, then reuse it instead of creating a duplicate. Do not reopen or reuse a closed or merged PR without explicit direction.

If the intended change set is empty, mixed with changes of uncertain ownership, or incomplete, stop before committing or pushing and explain the exact blocker.

## Prepare and verify the change

Before publication, confirm that the requested scope is complete, the base and head are correct, the full PR diff is coherent, and no known blocker is hidden.

Run repository-required formatting, lint, type, test, build, or validation commands at their required stage: before committing, after committing, after pushing, or after PR creation. Require checks that can run before publication to pass before creating or marking the PR ready. Checks that require a push or PR run after that prerequisite exists; report them as pending until results are available. If the repository specifies no checks for this change, use the smallest deterministic checks that exercise the changed behavior, with `git diff --check` on the intended diff as the minimum repository check.

Reuse recorded verification results when they can be tied to the code being published and the relevant dependencies, configuration, and environment still match. Run only missing or invalidated checks unless repository rules require a fresh run at the current stage; opening a PR is not itself a reason to repeat successful verification.

Record the exact commands and outcomes, distinguishing passed, failed, skipped, and unable-to-run checks. Confirm required coverage actually ran; a successful command that excluded it does not satisfy the publication check. A known required-check failure or unavailable required check blocks creating or marking the PR ready at that stage. Report the failure or gap; if a PR already exists, include its URL and leave it open. Never claim a test, review, or user journey that was not run. Preserve valid failing regressions; do not weaken tests, bypass the failing path, or reclassify required checks merely to publish. Resolve in-scope defects when authorized, or report the precise blocker.

If in-scope local changes remain, run checks required before committing, stage only the intended changes, inspect the staged diff, and create one clear commit for that completed work. Preserve existing commits unless the user explicitly requests a history change. Update the recorded head commit, recompute the complete base-to-head diff, and run checks required after committing. A commit with unchanged tested file contents does not invalidate evidence unless the check depends on Git metadata. If hooks change files, or verification depended on worktree changes absent from the commit, rerun the affected checks against the final revision.

## Author the pull request

Derive the title and body from the source issue or specification when available, the complete committed diff, the commit list, and the final verification results. Do not rely on conversation memory alone.

### Title

- Describe the outcome in simple, ordinary language.
- Make it understandable without reading the issue.
- Avoid vague wording such as "update logic" or "fix issue."
- Use repository prefixes such as `feat:` only when the repository requires them.

### Body

Follow the applicable repository template or the user's requested format. Preserve required sections and answer them accurately; omit optional sections that add no information. Do not mark template checkboxes complete without supporting evidence.

When no template governs, choose the structure the change warrants. A simple PR may need only a short explanation of the problem and resulting behavior, followed by verification commands and outcomes. Add implementation decisions, review pointers, compatibility risks, or non-goals only when they help assess the change. Avoid duplicate summaries, empty headings, and boilerplate such as a mandatory "None identified" risk section.

Keep every claim traceable to repository evidence. Do not invent scope, files, tests, risks, follow-up work, or success. Remove secrets, absolute local paths, private command output, and internal agent artifacts. Use repository-relative paths and concise result summaries.

Add `Closes #<number>` only when the PR fully completes that same-repository issue. Use a non-closing reference when the issue is only context or the work is partial. Do not infer issue numbers from branch names alone.

Write the reviewed Markdown to a temporary file outside the repository, or stream it through standard input when supported. Pass it with `--body-file`; do not interpolate multiline Markdown into a shell argument.

## Publish once

Require `gh` and successful authentication for the active account on the resolved host using `gh auth status --active --hostname HOST`.

Compare the remote head branch with the recorded head commit. Push only if that commit is not already the remote branch tip, using the resolved source ref and destination branch explicitly, without force. Confirm the source ref still identifies the recorded commit before pushing; if it moved, inspect and verify the new state first. Preserve existing upstream tracking configuration; publishing a PR does not require changing it.

For an existing matching PR, use `gh pr edit` with its URL and explicit title and `--body-file` arguments only when updates are needed. Preserve accurate human-authored context. Once the applicable checks pass, use `gh pr ready` with its URL if it is a draft. Do not call `gh pr create` for an existing open PR.

Otherwise create the PR with explicit arguments, including the resolved host in the repository identifier:

```bash
gh pr create \
  --repo HOST/OWNER/REPO \
  --base BASE_BRANCH \
  --head HEAD_BRANCH \
  --title "TITLE" \
  --body-file PR_BODY_FILE
```

For a fork, qualify the head as `OWNER:BRANCH`. Never pass `--draft`; this skill creates a real PR that is immediately ready for human and automated review.

If creation fails or returns unclear output, query GitHub for the exact head and base before retrying. Never blindly repeat a create operation. If the push succeeded but PR creation did not, preserve the pushed branch and report the partial state and exact error.

## Verify the published result

Read the created or reused PR back by URL with `gh pr view` and verify:

- it has a URL and number and is open
- `isDraft` is false
- repository, base branch, and head branch are exact
- GitHub's head commit matches the recorded, verified head commit
- title and body match the reviewed content

Inspect checks that require publication now that the PR exists. Return the PR URL and number, base and head, published commit, verification commands and outcomes, and any pending or failed checks or other disclosed limitation, then stop with the PR open for review. Do not manually close its source issue.
