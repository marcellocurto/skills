---
name: relentless-review
description: Challenge an existing proposal or result to find material risks and a better path.
---

# Relentless Review

Check whether the current proposal or result meets the requirements and whether a concrete alternative would improve it. Challenge assumptions and examine realistic failures. Recommend a different approach only when you can explain how it better meets the requirements or reduces a concrete risk.

A review request authorizes analysis and recommendations. Editing the artifact, implementing recommendations, or publishing changes requires authorization for those actions; reuse any authorization already given for the same scope.

## Goal

Give a direct verdict on whether to keep or change the current approach under the known requirements and constraints.

## Success Criteria

- State the requirements the result must meet.
- Identify assumptions that materially affect the verdict.
- Test relevant edge cases and failure modes.
- Compare the current approach against simpler, safer, more direct, or more reversible alternatives.
- Recommend keeping or changing the approach, with the reason.
- State what proof would change the verdict.

## Review Focus

Choose only the edge cases that matter for the artifact: empty, malformed, duplicate, large, slow, partial failure, race, stale state, permissions, versions, accessibility, timezone/localization, dependency failure, detectability, recovery, blast radius, and rollback.

## Evidence Budget

Use the available artifact and context first. Inspect more only when a material assumption, failure mode, alternative, or validation claim cannot be judged from what is already provided.

## Output

Lead with a direct verdict. Include or combine only the sections needed to explain it. Omit **Better path** when no alternative offers a concrete improvement.

- **Verdict**: direct judgment.
- **Why it may fail**: prioritized concerns with severity and confidence when useful.
- **Assumptions to challenge**: only the ones that matter.
- **Better path**: concrete recommendation.
- **Validation**: tests, checks, metrics, rollout guardrails, or evidence needed.

## Constraints

- Critique the work, not the person.
- Separate confirmed problems from plausible risks.
- Treat explicit business, product, and domain decisions as authoritative constraints unless the user asks to challenge them. Do not override them merely because another choice appears safer, simpler, more conventional, or less aggressive; distinguish risk analysis from authority to change the decision.
- Do not invent context or pad with generic warnings.
- Skip preferences and minor observations that do not affect the outcome. If no change is justified, say so and state any remaining limits.

## Stop Rules

Stop when the recommendation, relevant risks, and checks needed to support it are clear. Continue investigating only when a missing fact could change the recommendation; ask the user only when that fact cannot be established from available evidence.
