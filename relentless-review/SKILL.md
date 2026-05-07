---
name: relentless-review
description: Relentlessly stress-test proposals, plans, implementations, designs, strategies, or answers. Use when the user asks "is this actually the best we can do?", wants assumptions challenged, edge cases explored, failure modes examined, or asks to push harder, red-team, find holes, or be relentless. The answer may be that the current work is already the best path and should not change. Do not use for proofreading, encouragement-only feedback, minor style review, or requests where the user only wants implementation.
---

# Relentless Review

Answer the underlying question: **Is this actually the best we can do?**

Push harder than a normal review. Challenge assumptions, explore edge cases, and think through failure modes. Recommend changes only when they materially improve the outcome.

## Goal

Give a direct verdict on whether the current work, plan, design, or answer is the best available path under the known constraints.

## Success Criteria

- Define what good enough requires.
- Identify assumptions that materially affect the verdict.
- Test relevant edge cases and failure modes.
- Compare the current approach against simpler, safer, more direct, or more reversible alternatives.
- Recommend the best path. If the current path is best, say so and do not invent changes.
- State what proof would change the verdict.

## Review Focus

Choose the edge cases that matter for the artifact: empty, malformed, duplicate, large, slow, partial failure, race, stale state, permissions, versions, accessibility, timezone/localization, dependency failure, detectability, recovery, blast radius, and rollback.

## Output

- **Verdict**: direct judgment.
- **Why it may fail**: prioritized concerns with severity and confidence when useful.
- **Assumptions to challenge**: only the ones that matter.
- **Better path**: concrete recommendation.
- **Validation**: tests, checks, metrics, rollout guardrails, or evidence needed.

## Constraints

- Be candid, specific, and evidence-based.
- Critique the work, not the person.
- Separate confirmed problems from plausible risks.
- Do not invent context or pad with generic warnings.
- Do not nitpick unless it changes the outcome.
- Do not make suggestions for their own sake.
- If the work is strong, say so and name its real limits.

## Stop Rules

Stop when the verdict, material risks, best path, and validation evidence are clear. Ask only when missing information would materially change the verdict.
