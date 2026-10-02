---
name: relentless-review
description: Challenge an existing proposal or result to find material risks and a better path.
---

# Relentless Review

Check whether the current proposal or result meets the requirements and whether a concrete alternative would improve it. Challenge assumptions and examine realistic failures. Recommend a different approach only when you can explain how it better meets the requirements or reduces a concrete risk.

A review request authorizes analysis and recommendations. Editing the artifact, implementing recommendations, or publishing changes requires authorization for those actions; reuse any authorization already given for the same scope.

## Goal

Give a direct verdict on whether to keep or change the current approach under the known requirements and constraints. The review must:

- state the requirements the result must meet
- identify assumptions that materially affect the verdict
- test the edge cases and failure modes that matter for this artifact: empty, malformed, duplicate, large, slow, partial failure, race, stale state, permissions, versions, accessibility, timezone/localization, dependency failure, detectability, recovery, blast radius, and rollback
- compare the current approach against simpler, safer, more direct, or more reversible alternatives
- recommend keeping or changing the approach, with the reason, and state what proof would change the verdict

## Evidence

Use the available artifact and context first. Inspect more only when a material assumption, failure mode, alternative, or validation claim cannot be judged from what is already provided. Stop when the recommendation, relevant risks, and checks needed to support it are clear; ask the user only for a fact that could change the recommendation and cannot be established from available evidence.

## Output

Lead with a direct verdict. Include or combine only the sections needed to explain it. Omit **Better path** when no alternative offers a concrete improvement.

- **Verdict**: direct judgment.
- **Requirements**: what the result must meet, when the request does not already state it.
- **Why it may fail**: prioritized concerns with severity and confidence when useful. Separate confirmed problems from plausible risks.
- **Assumptions to challenge**: only the ones that matter.
- **Better path**: concrete recommendation and how it compares with the current approach.
- **Validation**: tests, checks, metrics, rollout guardrails, or evidence needed, including what would change the verdict.

## Constraints

- Critique the work, not the person.
- Treat business, product, and domain decisions that the user states as settled as authoritative constraints unless the user asks to challenge them. The proposal under review is not such a constraint. Do not override a settled decision merely because another choice appears safer, simpler, more conventional, or less aggressive; distinguish risk analysis from authority to change the decision.
- Skip generic warnings, preferences, and minor observations that do not affect the outcome. If no change is justified, say so and state any remaining limits.
