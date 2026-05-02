---
name: issue-fix-plan
description: Write a detailed, comprehensive plan to fix an issue. Use when the user asks for a fix plan, implementation plan, remediation plan, or says to plan how to fix a bug/issue. Where details are missing or uncertain, reason through them, state assumptions, and propose the smartest practical solution.
---

# Issue Fix Plan

Produce a clear, comprehensive plan for fixing an issue. This skill plans the work; do not edit code unless the user explicitly asks to implement.

## Inputs

Use all available context: the user's description, pasted issue text, errors/logs, screenshots, files, code references, or GitHub issue links/numbers.

If a GitHub issue is referenced and the repo is available, inspect it first:

```bash
gh issue view <number-or-url> --comments
```

Ask follow-up questions only when a missing detail blocks a useful plan. Otherwise infer the smartest approach, label it as an assumption, and continue.

## Plan Structure

Write the plan with these sections, omitting only sections that truly do not apply:

1. **Goal** — what fixed means in one or two sentences.
2. **Current Understanding** — facts from the issue/context.
3. **Assumptions & Unknowns** — inferred details, risks, and what should be verified.
4. **Root Cause Hypothesis** — likely cause(s) and how to confirm them.
5. **Proposed Solution** — the recommended fix and why it is the best option.
6. **Implementation Steps** — ordered, concrete steps with files/modules to inspect or change when known.
7. **Validation Plan** — tests, manual checks, regression coverage, and edge cases.
8. **Risks & Rollback** — likely failure modes, compatibility concerns, and rollback strategy.
9. **Acceptance Criteria** — concise checklist proving the issue is fixed.

## Guidance

- Be decisive: choose a best path instead of listing vague alternatives.
- Be explicit about reasoning where details are missing.
- Keep scope focused on fixing the issue; do not add unrelated refactors or features.
- Prefer minimal safe changes unless the issue clearly requires deeper redesign.
- Include investigation steps before implementation when the root cause is uncertain.
- Make validation specific enough that another engineer can execute it.
- If multiple fixes are possible, recommend one and briefly explain why others are weaker.

## Output Style

Use Markdown headings and checklists. The plan should be detailed enough for an engineer to implement without needing the original conversation, but concise enough to stay actionable.
