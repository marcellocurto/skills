---
name: create-pull-request
description: Open a ready-for-review GitHub pull request for completed local changes, including any needed commit and push.
---

# Create Pull Request

Publish one completed change as a clear, accurate, ready-for-review GitHub pull request.

A direct request to create, open, or publish the PR authorizes the ordinary commit, push, and PR creation needed for that exact change. It does not authorize force-pushing, merging, issue edits, labels, reviewers, assignees, or unrelated local changes.

## Establish the change

- Read the repository instructions for branches, commits, verification, and pull requests.
- Resolve the exact repository, push remote, base branch, and head branch from the user's request, repository instructions, Git remotes, and GitHub's default branch. Do not guess when these disagree.
- Inspect the complete merge-base diff against the fetched base branch, its commits, staged and unstaged changes, untracked files, and `git diff --check`.
- Refuse to publish from a detached HEAD or directly from the base or another protected branch. If completed work is still on the base branch, create a task-specific branch using repository naming rules.
- Preserve unrelated worktree changes. Stage only clearly in-scope paths; never stash, discard, clean, reset, amend, rebase, or rewrite history merely to publish the PR.
- Check for an existing open PR with the same repository, base, and head. Reuse and verify it instead of creating a duplicate. Do not reopen or reuse a closed or merged PR without explicit direction.

If the intended change set is empty, mixed with changes of uncertain ownership, or incomplete, stop before committing or pushing and explain the exact blocker.

## Apply the publication gates

Publish only when both gates pass:

1. **Readiness:** the requested scope is complete, the base and head are correct, the full PR diff is coherent, and no known blocker is hidden.
2. **Verification:** repository-required formatting, lint, type, test, build, or validation commands pass. Otherwise run the smallest deterministic checks that exercise the changed behavior, with `git diff --check` as the minimum repository check.

Record the exact commands and outcomes. Never claim a test, review, or user journey that was not run. If a required check fails, do not create the PR and do not change the implementation merely to force the gate green. Report the failure and leave the work recoverable.

If local changes remain after the gates pass, stage the exact in-scope paths, inspect the staged diff, and create one clear commit for that completed work. Preserve existing commits unless the user explicitly requests a history change. Recompute the complete base-to-head diff after committing.

## Author the pull request

Derive the title and body from the source issue or specification when available, the complete committed diff, the commit list, and the final verification results. Do not rely on conversation memory alone.

### Title

- Describe the outcome in simple, ordinary language.
- Make it understandable without reading the issue.
- Avoid vague wording such as "update logic" or "fix issue."
- Use repository prefixes such as `feat:` only when the repository requires them.

### Body

Use this stable structure:

```markdown
## Summary

<Explain what changed, why it matters, and the resulting behavior in two or three clear sentences.>

## Detailed description

- <Important behavior change>
- <Important implementation detail or design decision>

## How to review

- <Where the reviewer should start or what deserves close attention>

## Verification

- `<exact command>` — passed

## Risks and non-goals

- <Known risk, limitation, explicit non-goal, or "None identified.">
```

Keep every claim traceable to repository evidence. Do not invent scope, files, tests, risks, follow-up work, or success. Remove secrets, absolute local paths, private command output, and internal agent artifacts. Use repository-relative paths and concise result summaries.

Add `Closes #<number>` only when the PR fully completes that same-repository issue. Use a non-closing reference when the issue is only context or the work is partial. Do not infer issue numbers from branch names alone.

Write the reviewed Markdown to a temporary file outside the repository, or stream it through standard input when supported. Pass it with `--body-file`; do not interpolate multiline Markdown into a shell argument.

## Publish once

Require `gh` and a successful `gh auth status`, then push the exact current branch and set its upstream without force. Create the PR with explicit arguments:

```bash
gh pr create \
  --repo OWNER/REPO \
  --base BASE_BRANCH \
  --head HEAD_BRANCH \
  --title "TITLE" \
  --body-file PR_BODY_FILE
```

For a fork, qualify the head as `OWNER:BRANCH`. Never pass `--draft`; this skill creates a real PR that is immediately ready for human and automated review.

If creation fails or returns unclear output, query GitHub for the exact head and base before retrying. Never blindly repeat a create operation. If the push succeeded but PR creation did not, preserve the pushed branch and report the partial state and exact error.

## Verify the published result

Read the PR back with `gh pr view` and verify:

- it has a URL and number and is open
- `isDraft` is false
- repository, base branch, and head branch are exact
- GitHub's head commit matches local `HEAD`
- title and body match the reviewed content

Return the PR URL and number, base and head, published commit, verification commands and outcomes, and any disclosed limitation. Do not merge the PR or manually close its source issue.
