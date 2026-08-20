---
name: relentless-review
description: Stress-test proposals, plans, implementations, designs, strategies, or answers. Use when the user asks to push harder, red-team, find holes, challenge assumptions, explore failure modes, or decide whether the current path is genuinely best. Not for proofreading or implementation-only requests.
---

# Relentless Review

Answer the underlying question: **Is this actually the best we can do?**

Challenge assumptions, explore edge cases, and think through failure modes. Recommend changes only when they materially improve the outcome.

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

Choose only the edge cases that matter for the artifact: empty, malformed, duplicate, large, slow, partial failure, race, stale state, permissions, versions, accessibility, timezone/localization, dependency failure, detectability, recovery, blast radius, and rollback.

## Evidence Budget

Use the available artifact and context first. Inspect more only when a material assumption, failure mode, alternative, or validation claim cannot be judged from what is already provided.

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
- Treat explicit business, product, and domain decisions as authoritative constraints unless the user asks to challenge them. Do not override them merely because another choice appears safer, simpler, more conventional, or less aggressive; distinguish risk analysis from authority to change the decision.
- Do not invent context or pad with generic warnings.
- Do not nitpick unless it changes the outcome.
- Do not make suggestions for their own sake.
- If the work is strong, say so and name its real limits.

## Stop Rules

Stop when the verdict, material risks, best path, and validation evidence are clear. Ask only when missing information would materially change the verdict.
