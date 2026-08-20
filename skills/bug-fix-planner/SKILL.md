---
name: bug-fix-planner
description: Investigate one bug and produce an implementation-ready fix plan without changing code.
---

# Bug Fix Planner

Plan the smallest credible fix for one specific defect.

Plan only. Do not edit files, apply patches, commit, or implement unless the user explicitly asks.

## Goal

Give another engineer enough evidence and direction to fix the bug without rereading the conversation.

## Success Criteria

- The broken behavior, expected behavior, impact, and affected area are clear.
- Important claims are classified as **Confirmed**, **Likely**, or **Unknown**.
- The plan traces the failing path in real code when repository access exists.
- The recommendation names one primary fix path, not a loose option list.
- Reproduction and validation preserve the user's entry point, environment, inputs, and sequence when they affect the defect, and acceptance criteria prove the original behavior is fixed.

## Constraints

- Keep scope limited to the defect.
- Prefer the smallest change that fixes the root cause and matches existing code patterns.
- Do not recommend redesigns, unrelated cleanup, broad refactors, migrations, or workaround-only fixes unless the evidence shows a local fix cannot work.
- Do not replace the user's path with a more convenient lower-level reproduction or validation when it can bypass the reported failure.
- Do not recommend removing the visible symptom when the evidence points to a deeper mismatch. Establish the mechanism and fix the root cause, or make verifying it the first plan step.
- Do not recommend tests that only mirror implementation.

## Evidence Budget

Start with the user's evidence: issue text, logs, stack traces, screenshots, repro steps, failing tests, referenced files, entry point, environment, inputs, and action sequence. Inspect source when repo access exists and the failing path, likely cause, or validation path is unclear.

Use the minimum evidence needed to name a leading cause, one primary fix, and validation. Continue looking only when a required fact, failing path, root-cause check, or validation path is missing.

Ask only when missing information prevents a useful plan. Otherwise state assumptions and continue.

## Output

Include the evidence, uncertainty, validation, and material caveats needed to make the plan implementable. Omit unused sections and repeated background.

- **Goal**: what fixed means.
- **Evidence**: confirmed facts, likely facts, unknowns.
- **Reproduction**: exact user-observed path, or how to establish it first without bypassing the failure.
- **Root cause**: confirmed cause, or leading hypothesis plus verification.
- **Fix plan**: files/functions to change, what to change, and why this solves it.
- **Steps**: ordered implementation steps.
- **Validation**: the original path plus useful lower-level tests, new regression coverage, manual checks, and edge cases.
- **Risks**: blast radius, compatibility concerns, rollback if relevant.
- **Acceptance criteria**: short checklist proving the bug is fixed.

## Stop Rules

Stop when the plan identifies the leading cause, one primary fix, and checks that would prove the defect is gone. If repo access or reproduction is unavailable, say so and make closing that gap the first step.
