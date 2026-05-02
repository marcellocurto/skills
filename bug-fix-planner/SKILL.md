---
name: bug-fix-planner
description: Plan how to fix a specific bug, regression, or defect without implementing it. Trigger when the user asks to plan a fix, hands over a bug report, GitHub issue, error, stack trace, failing test, or crash log and wants a path forward, or describes broken behavior and asks what to do. Do NOT trigger for new features, unrelated refactors, or when the user wants the bug fixed immediately.
---

# Bug Fix Planner

Produce a clear, actionable plan for fixing a specific bug or defect. **Plan only — do not modify code unless the user explicitly asks to implement.**

## Investigate Before Planning

1. Read all available context: user description, issue text, errors, logs, screenshots, files, and code references.
2. If a GitHub issue is referenced and `gh` is available, run:

   ```bash
   gh issue view <number-or-url> --comments
   ```

3. Read the relevant code and trace the failing path. Do not plan against imagined code.
4. Identify repro steps or a failing test. If you cannot reproduce, say so and make reproduction the first implementation step.
5. Separate symptom from cause; the fix should target the cause.

Ask clarifying questions only when missing information blocks a useful plan. Otherwise make the smartest assumption, label it, and continue.

## Plan Structure

Scale depth to the issue. A typo fix may need only a few short sections; a subtle race condition may need all of them. Drop sections that do not apply.

1. **Goal** — what “fixed” means in one or two sentences.
2. **Current understanding** — where it manifests, impact, and relevant files, lines, or logs.
3. **Reproduction** — exact steps or failing test; if unknown, how to establish one.
4. **Root cause** — confirmed cause with evidence, or a clearly labeled hypothesis plus how to confirm it.
5. **Assumptions and open questions** — inferred details to verify during implementation.
6. **Proposed fix** — recommended change, files/functions involved, and rationale.
7. **Alternatives considered** — only when a real trade-off exists; explain why rejected.
8. **Implementation steps** — ordered, concrete steps an engineer can follow.
9. **Validation** — tests, manual checks, regression coverage, and edge cases.
10. **Risks and rollback** — blast radius, compatibility concerns, and revert strategy.
11. **Acceptance criteria** — short checklist proving the bug is fixed.

## Choosing the Fix

Prefer, in order:

1. Correctness
2. Minimal scope
3. Low risk
4. Fit with existing code patterns

Recommend the smallest change that resolves the root cause. Use deeper redesign only when a surface fix would leave the real defect intact.

## Anti-Patterns

- Listing vague options instead of picking a recommended path.
- Padding with generic advice that does not reference this bug.
- Planning without inspecting relevant code.
- Expanding scope into unrelated refactors or cleanups.
- Treating an unverified hypothesis as fact.
- Skipping validation because the fix “looks obvious.”

## Output

Write Markdown with headings and checklists. The plan should stand alone so another engineer can implement it without reading the original conversation. Aim for actionable density, not length.
