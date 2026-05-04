---
name: relentless-review
description: Relentlessly stress-test proposals, plans, implementations, designs, strategies, or answers. Use when the user asks "is this actually the best we can do?", wants assumptions challenged, edge cases explored, failure modes examined, or asks to push harder, red-team, find holes, or be relentless. The answer may be that the current work is already the best path and should not change. Do not use for proofreading, encouragement-only feedback, minor style review, or requests where the user only wants implementation.
---

# Relentless Review

Answer the underlying question: **Is this actually the best we can do?**

Push harder than a normal review. Challenge assumptions, explore edge cases, and think through failure modes. Recommend changes only when they materially improve the outcome.

## Review

1. Define what good enough requires.
2. Identify assumptions and what breaks if they are false.
3. Test edge cases: empty, malformed, duplicate, large, slow, partial failure, race, stale state, permissions, versions, accessibility, timezone/localization, dependency failure.
4. Analyze failure modes: detectability, recovery, blast radius, rollback.
5. Compare the current approach against simpler, safer, more direct, or more reversible alternatives.
6. Recommend the best path. If the current path is best, say so and do not invent changes.
7. State what proof would change the verdict.

## Output

- **Verdict**: direct judgment.
- **Why it may fail**: prioritized concerns with severity and confidence when useful.
- **Assumptions to challenge**: only the ones that matter.
- **Better path**: concrete recommendation.
- **Validation**: tests, checks, metrics, rollout guardrails, or evidence needed.

## Rules

- Be candid, specific, and evidence-based.
- Critique the work, not the person.
- Separate confirmed problems from plausible risks.
- Do not invent context or pad with generic warnings.
- Do not nitpick unless it changes the outcome.
- Do not make suggestions for their own sake.
- If the work is strong, say so and name its real limits.
