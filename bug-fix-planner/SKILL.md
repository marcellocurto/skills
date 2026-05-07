---
name: bug-fix-planner
description: Plan a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code. Use when the user wants a path forward from a bug report, GitHub issue, stack trace, logs, screenshots, repro steps, or failing test. Do not use for new features, broad refactors, general debugging advice, or requests to directly implement the fix.
---

# Bug Fix Planner

Create an evidence-based fix plan for one specific defect.

Plan only. Do not edit files, apply patches, commit, or implement unless the user explicitly asks.

## Goal

A good plan lets another engineer fix the bug without rereading the conversation. It identifies what is broken, why it is likely broken, the smallest safe fix, and how to prove it works.

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

Use the minimum evidence needed to make a useful plan. Inspect issue text, logs, stack traces, screenshots, repro steps, failing tests, referenced files, and relevant source. Continue looking only when a required fact, failing path, root-cause check, or validation path is missing.

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

Stop when the plan has enough evidence to identify the leading cause, one primary fix, and validation. If repo access or reproduction is unavailable, say so and make closing that gap the first step.
