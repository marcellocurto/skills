---
name: relentless-review
description: Relentlessly challenge a proposal, plan, implementation, or answer. Use when the user asks whether this is the best possible approach, wants assumptions challenged, edge cases explored, failure modes identified, or says to push harder / be relentless.
---

# Relentless Review

Stress-test the current answer, plan, design, or implementation. Push beyond surface-level critique and identify what could break, what was assumed, and what a stronger solution would look like.

## When to Use

Use this skill when the user asks things like:

- "Is this actually the best we can do?"
- "Challenge the assumptions."
- "Explore the edge cases."
- "Think through failure modes."
- "Push harder."
- "Be relentless."
- "What are we missing?"

## Review Method

Evaluate the work from multiple angles:

1. **Goal fit** — does the solution actually solve the real problem, or just the stated symptom?
2. **Assumptions** — what is being assumed, and what happens if those assumptions are false?
3. **Edge cases** — unusual inputs, scale, timing, permissions, empty states, partial failures, malformed data, and user misuse.
4. **Failure modes** — how the solution can fail, how visible failures are, and whether recovery is possible.
5. **Tradeoffs** — complexity, maintainability, performance, security, UX, compatibility, and operational cost.
6. **Alternatives** — stronger or simpler approaches that may have been skipped.
7. **Proof** — what evidence, tests, monitoring, or experiments would validate the choice.

## Output Structure

Use this structure unless another format is requested:

```markdown
## Short Verdict

<Direct answer: acceptable, risky, overbuilt, underbuilt, or not good enough.>

## Biggest Concerns

1. <Concern, why it matters, consequence if ignored>
2. <Concern, why it matters, consequence if ignored>

## Assumptions to Challenge

- <Assumption> → <How to verify or what to do if false>

## Edge Cases & Failure Modes

- <Case/failure> → <Expected behavior or mitigation>

## Better Approach

<Recommended changes or alternative plan. Be decisive.>

## Validation

- [ ] <Test/check/experiment that proves the solution works>
- [ ] <Test/check/experiment that catches the risky case>

## Final Recommendation

<What to do next.>
```

## Rules

- Be candid and specific; avoid generic warnings.
- Do not nitpick style unless it affects correctness, maintainability, or user impact.
- Separate known facts from speculation.
- If the current approach is good, say so—but still identify its real limits.
- Prefer actionable fixes over criticism-only feedback.
- Do not ask questions as a substitute for analysis unless a missing fact truly blocks judgment.
