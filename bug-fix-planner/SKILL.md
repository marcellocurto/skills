---
name: bug-fix-planner
description: Plan a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code. Use when the user wants a path forward from a bug report, GitHub issue, stack trace, logs, screenshots, repro steps, or failing test. Do not use for new features, broad refactors, general debugging advice, or requests to directly implement the fix.
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
- Validation and acceptance criteria prove the original defect is gone.

## Constraints

- Keep scope limited to the defect.
- Prefer the smallest change that fixes the root cause and matches existing code patterns.
- Do not recommend redesigns, unrelated cleanup, broad refactors, migrations, or workaround-only fixes unless the evidence shows a local fix cannot work.
- Do not recommend tests that only mirror implementation.

## Evidence Budget

Start with the user's evidence: issue text, logs, stack traces, screenshots, repro steps, failing tests, and referenced files. Inspect source when repo access exists and the failing path, likely cause, or validation path is unclear.

Use the minimum evidence needed to name a leading cause, one primary fix, and validation. Continue looking only when a required fact, failing path, root-cause check, or validation path is missing.

Ask only when missing information prevents a useful plan. Otherwise state assumptions and continue.

## Output

Use concise Markdown. Include only relevant sections.

- **Goal**: what fixed means.
- **Evidence**: confirmed facts, likely facts, unknowns.
- **Reproduction**: exact repro or how to establish it first.
- **Root cause**: confirmed cause, or leading hypothesis plus verification.
- **Fix plan**: files/functions to change, what to change, and why this solves it.
- **Steps**: ordered implementation steps.
- **Validation**: existing tests, new regression coverage, manual checks, edge cases.
- **Risks**: blast radius, compatibility concerns, rollback if relevant.
- **Acceptance criteria**: short checklist proving the bug is fixed.

## Stop Rules

Stop when the plan identifies the leading cause, one primary fix, and checks that would prove the defect is gone. If repo access or reproduction is unavailable, say so and make closing that gap the first step.
