---
name: address-review-feedback
description: Evaluate pull-request review feedback, implement justified fixes, and reply to and resolve addressed threads.
---

# Address Review Feedback

Work through PR feedback using independent judgment. Evaluate claims against the user's latest decisions, accepted PR requirements, and repository guidance. A reviewer's confidence, repetition, bot identity, or supplied patch is not evidence that a change is needed or correct.

## Scope and authorization

An audit-only request stays read-only: report assessments and proposed fixes. A request to fix feedback authorizes justified, in-scope local changes. A request to **address and resolve PR feedback** also authorizes the necessary commits, pushes, thread replies, and resolutions. Reuse prior authorization without asking again per thread; honor requests to review proposals before implementation. Ask only for missing decisions or operations outside the authorized scope, and continue independent work while waiting.

Do not force-push, merge, submit a review, change PR metadata, or create follow-up issues under this workflow unless explicitly requested. Preserve unrelated work and the existing branch; explain and obtain permission before creating or switching branches unless already explicitly authorized.

## Establish the PR

- Resolve the exact PR and GitHub host from its URL, repository and number, or current branch. Before editing, verify the checkout represents its head repository, branch, and current commit.
- Read thread-aware context through an available connector or `python "<skill-path>/scripts/fetch_review_context.py"`. Pass `--pr URL` or `--repo HOST/OWNER/REPO --pr NUMBER`; omit both for the current branch PR. Unqualified `OWNER/REPO` uses `GH_HOST`, otherwise `github.com`.
- Retain the host for all operations. The helper checks `gh auth status --active --hostname HOST`; diagnose only the target account's failure and request login only when authentication needs repair.
- Cover every unresolved review thread, including outdated ones. Consult resolved threads, review summaries, and general PR comments when they contain relevant context or separate actionable feedback. Track each source so none is silently skipped.

## Work through the feedback

For each thread:

1. **Validate the concern.** Read the entire conversation and inspect the current code, PR diff, requirements, repository guidance, and relevant callers or tests. Identify the actual failure, contract violation, or concrete maintenance cost. Separate established facts from assumptions; missing evidence means uncertainty, not automatic acceptance or dismissal.
2. **Judge the remedy independently.** Check whether the suggestion addresses the cause, preserves intended behavior, fits the codebase, and earns its complexity. A valid concern can have a poor remedy: choose a better fix. Optional preferences do not become requirements merely because a reviewer proposed them. Decline unnecessary or counterproductive changes with concrete reasoning.
3. **Act on the assessment.** For a justified, in-scope fix, briefly explain the proposed implementation and why it fits, then implement when authorized. Verify the changed behavior and recheck the resulting diff; reuse still-valid verification and add tests only for realistic regressions. For invalid, already-addressed, or unjustified optional suggestions, make no code change. Leave uncertain, incomplete, failed-verification, or undecided scope questions open and explain what is needed.
4. **Reply and resolve when authorized.** For a fix, commit only the intended changes and push to the PR's actual head without force. Confirm GitHub contains the verified commit before claiming the fix is published. Reply in the original thread with the outcome, concise evidence or reasoning, and the commit and verification for a fix. For declined or already-addressed feedback, explain why no change is needed. Resolve only after the reply succeeds and every concern in that thread has a supported disposition; unresolved work or an unapproved deferral keeps it open.

Related concerns may share an implementation, commit, or verification run, but reply to each original thread. General PR comments have no thread-resolution state; respond where appropriate without claiming to resolve them.

Before a reply or resolution, refresh the thread and relevant PR head to catch intervening changes. Preserve others' work, skip already-completed operations, and read back uncertain outcomes before retrying to avoid duplicate replies. Verify each reply and resolution; report publication failures without claiming completion.

Finish with a short summary of fixes, declined or already-addressed feedback, and remaining open threads with their blockers. Link the PR and relevant commits; disclose missing coverage. Do not create a large classification report unless requested.
