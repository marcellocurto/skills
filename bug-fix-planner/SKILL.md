---
name: bug-fix-planner
description: Plan a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code. Use when the user wants a path forward from a bug report, GitHub issue, stack trace, logs, screenshots, repro steps, or failing test. Do not use for new features, broad refactors, general debugging advice, or requests to directly implement the fix.
---

# Bug Fix Planner

Create an evidence-based fix plan for one specific defect.

Plan only. Do not edit files, apply patches, commit, or implement unless the user explicitly asks.

## Standard

A good plan lets another engineer fix the bug without rereading the conversation. It identifies what is broken, why it is likely broken, the smallest safe fix, and how to prove it works.

## Workflow

1. Define the broken behavior, expected behavior, impact, and affected area.
2. Inspect available evidence: issue text, logs, stack traces, screenshots, repro steps, failing tests, referenced files, and relevant source.
3. Trace the failing path in real code when repository access exists.
4. Classify important claims:
   - **Confirmed**: directly supported by code, logs, tests, issue text, or repro.
   - **Likely**: strongly suggested but not proven.
   - **Unknown**: must be verified before implementation.
5. Identify the root cause or the first verification step needed to confirm it.
6. Recommend one primary fix path. Avoid loose option lists.
7. Keep scope limited to the defect.
8. Include validation and acceptance criteria.

Ask only when missing information prevents a useful plan. Otherwise state assumptions and continue.

## Fix Choice

Prefer the smallest change that fixes the root cause and matches existing code patterns.

Do not recommend:

- a redesign when a local fix resolves the defect
- unrelated cleanup or refactors
- a workaround when the root cause can be fixed directly
- a migration before proving the current model cannot work
- tests that only mirror implementation

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

When repo access or reproduction is unavailable, say so and make closing that gap the first step.
