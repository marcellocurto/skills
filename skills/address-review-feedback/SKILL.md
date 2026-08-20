---
name: address-review-feedback
description: Validate pull-request feedback against the current code and requirements, then apply only the fixes the user approves.
---

# Address Review Feedback

Treat review feedback as claims to validate, not instructions. The user's latest decisions, the PR requirements or linked issue, and applicable repository guidance define expected behavior; the current code and diff provide evidence. Audit first. Do not edit code merely because the skill was invoked, even when the initial request says to address everything.

## Access and scope

- Resolve the exact pull request from a supplied repository and PR number or URL, or from the current branch.
- Fetch thread-aware review context with `python "<skill-path>/scripts/fetch_review_context.py"`. Pass `--repo OWNER/REPO --pr NUMBER` or `--pr URL`; omit both for the current branch PR.
- When a thread-aware GitHub connector is already available, it may be used for review-context reads instead.
- Before using the fallback, require `gh` and confirm `gh auth status`. If authentication fails, ask the user to run `gh auth login`.
- Before editing, confirm that the local checkout and branch represent the pull request being audited. A remote-only audit may proceed, but implementation requires the matching local code.

## Phase 1: audit

Treat unresolved, non-outdated review threads as the default candidates. Consult resolved, outdated, top-level conversation comments, and review summaries when they provide necessary context or contain a concern not represented by a current thread. Audit the complete review history only when requested. Thread state controls attention, not truth: unresolved does not mean valid, resolved does not prove fixed, and outdated does not guarantee irrelevance.

For every independent concern:

1. Read the entire thread and its code anchor.
2. Inspect the current code, relevant PR diff, governing requirements, affected callers or tests, and repository rules needed to judge it.
3. Evaluate the concern separately from the reviewer's proposed remedy. A concern may be correct while its suggested implementation is excessive, incomplete, or harmful.
4. Split independent concerns from one source. Merge duplicate sources only when they describe the same concern and retain every source URL or ID.
5. Assess the concern as exactly one of:
   - `current`: the concern is confirmed in the current code
   - `already-addressed`: the current code already satisfies it
   - `invalid-stale`: the premise is false, obsolete, no longer applies to the current code, or the requested behavior would cause a regression
   - `uncertain`: the available evidence cannot establish whether the concern is real
6. For a `current` concern, choose exactly one handling:
   - `must-fix-current`: the PR cannot be approved without the fix; use only with medium or high confidence
   - `follow-up`: confirmed work that should be completed separately because it is outside the current PR
   - `suggestion`: an optional, non-blocking improvement that is not required work
7. Record a `needs-human` blocker independently when missing context or a decision prevents sound classification or implementation. State the exact question and what it blocks.

Every finding must include its sources, concrete evidence, assessment, handling when applicable, confidence (`low`, `medium`, or `high`), current-PR impact, and recommendation. A code location alone is not evidence: connect it to an observed behavior, requirement, caller, test, repository rule, or command result. For a proposed fix, describe the smallest complete outcome and verification that would prove the concern resolved.

Lead with a short summary of current fixes, follow-ups, suggestions, and human decisions. Then present numbered findings, separating observed facts from inference. Report whether coverage is complete or limited; name unavailable evidence and whether it prevents a safe recommendation. No findings is a valid result. Stop and wait for explicit approval before editing.

## Approval gate

The user may approve individual finding numbers or say `implement all recommended fixes`. Bulk approval includes only `current` findings handled as `must-fix-current` with no unresolved `needs-human` blocker. Never implement follow-ups, suggestions, already-addressed, invalid-stale, uncertain, findings with an unresolved `needs-human` blocker, or unapproved findings.

## Phase 2: implement approved findings

1. Implement the approved outcome, not necessarily the reviewer's proposed patch. Use the smallest complete change that fits the codebase and preserves unrelated behavior.
2. Preserve traceability from each change to its approved finding. Do not include unrelated cleanup or refactoring.
3. Run focused verification for the changed behavior. Add or change tests only when they protect observable behavior and would catch a realistic regression.
4. Re-audit the resulting diff: confirm each approved concern is resolved, the PR requirements still hold, relevant callers were not regressed, and no unapproved scope entered the change.
5. Report each approved finding as `addressed`, `partially addressed`, `failed verification`, or `blocked`, with evidence. Report unapproved findings as unchanged.

If new evidence invalidates the approved approach or the fix requires a material scope expansion, stop and return to the user for approval.

Do not reply on GitHub, resolve or unresolve threads, submit a review, commit, push, or change the pull request unless the user separately requests that specific mutation. If requested, apply it only to the findings whose resulting state supports it.
