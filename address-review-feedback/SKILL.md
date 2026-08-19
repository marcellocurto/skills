---
name: address-review-feedback
description: Audit GitHub pull-request review feedback against the current code, recommend a disposition for each finding, and implement only user-approved fixes. Use only when explicitly invoked for review follow-up.
---

# Address Review Feedback

Audit first. Do not edit code merely because the skill was invoked, even when the initial request says to address everything.

## Access and scope

- Resolve the exact pull request from a supplied repository and PR number or URL, or from the current branch.
- Fetch thread-aware review context with `python "<skill-path>/scripts/fetch_review_context.py"`. Pass `--repo OWNER/REPO --pr NUMBER` or `--pr URL`; omit both for the current branch PR.
- When a thread-aware GitHub connector is already available, it may be used for review-context reads instead.
- Before using the fallback, require `gh` and confirm `gh auth status`. If authentication fails, ask the user to run `gh auth login`.
- Before editing, confirm that the local checkout and branch represent the pull request being audited. A remote-only audit may proceed, but implementation requires the matching local code.

## Phase 1: audit

Treat unresolved, non-outdated review threads as the default candidates. Consult resolved, outdated, duplicate, top-level conversation comments, and review summaries only when they provide necessary context or contain actionable feedback not represented by a thread. Audit the complete review history only when requested.

For every candidate:

1. Read the entire thread and its code anchor.
2. Inspect the current code and relevant diff. An unresolved GitHub thread may already be addressed in code.
3. Group comments only when they have the same disposition, while preserving every source thread URL or ID.
4. Classify the finding as exactly one of:
   - `actionable`: the feedback is correct, still relevant, and should cause a change
   - `already addressed`: the current code satisfies the feedback even though the thread remains unresolved
   - `not actionable`: the premise is false, the request duplicates other feedback, is obsolete or out of scope, or would regress behavior
   - `unclear`: evidence is insufficient or human judgment is required
5. Recommend a disposition. For actionable findings, describe the smallest credible fix and verification. For other findings, explain why no change should occur or what must be clarified.

Present numbered findings with their source threads, evidence, classification, and recommendation. Separate observed facts from inference. Stop and wait for explicit approval before editing.

## Approval gate

The user may approve individual finding numbers or say `implement all recommended fixes`. Bulk approval includes only findings classified as actionable. Never implement unclear, already-addressed, not-actionable, or unapproved findings.

## Phase 2: implement approved findings

1. Make only the approved local changes, preserving traceability from each change to its finding.
2. Run focused verification for the changed behavior.
3. Re-audit every approved finding against the resulting code.
4. Report each approved finding as `addressed`, `partially addressed`, `failed verification`, or `blocked`, with evidence.
5. Report unapproved findings as unchanged.

Do not reply on GitHub, resolve or unresolve threads, submit a review, commit, push, or change the pull request unless the user separately requests that specific mutation. If requested, apply it only to the findings whose resulting state supports it.
