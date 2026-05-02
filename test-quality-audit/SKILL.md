---
name: test-quality-audit
description: Audit tests for real bug-finding value. Use when the user asks whether tests are useful, trivial, redundant, over-mocked, implementation-coupled, snapshot-heavy, coverage-padding, only passing because the test controls both sides, or whether tests should be kept, fixed, cut, or added. Also use when reviewing test changes in a PR and the user wants honest judgment about whether the tests earn their place.
---

# Test Quality Audit

Ruthlessly audit tests for signal.

Keep tests that protect meaningful behavior. Fix or cut tests that only mirror implementation, assert trivia, test mocks instead of behavior, duplicate the code under test, or exist mainly to increase coverage numbers.

The goal is not “more tests.” The goal is a smaller, stronger suite that catches real regressions.

## Core Standard

A test earns its place only if it can answer:

> “What realistic bug or regression would this catch?”

If that answer is vague, trivial, or entirely controlled by the test itself, the test is weak.

For every important test or test group, evaluate:

1. What behavior does this protect?
2. What bug would make it fail?
3. Would that bug matter to a user, caller, system, or maintainer?
4. Could the implementation be broken while this test still passes?
5. Could a harmless refactor break this test?
6. Is this the right testing level: unit, integration, contract, end-to-end, or none?

## When to Use

Use this skill when the user asks questions like:

- “Are these tests actually useful?”
- “Did these tests catch anything non-obvious?”
- “Are these tests too mocked?”
- “Should we cut these tests?”
- “Are we just testing implementation details?”
- “Is this coverage meaningful?”
- “Be honest about the test quality.”
- “Which tests should stay, change, or go?”
- “Review this PR’s tests.”
- “Are these snapshots worth keeping?”

## What to Inspect

Before judging the tests, inspect enough context to understand the real risk:

- the implementation under test
- the public API or user-visible behavior
- relevant branches and failure modes
- fixtures, mocks, factories, snapshots, and test helpers
- existing tests for the same behavior
- recent bug reports, regressions, or PR intent when available
- external boundaries such as databases, APIs, queues, auth, filesystems, time, randomness, or network calls

Do not audit tests in isolation when the implementation is available. A test can look reasonable alone and still be useless against the actual code.

## Audit Method

For each test file, test case, or logical test group:

1. Identify what the test claims to verify.
2. Identify what behavior it actually verifies.
3. Identify what kind of bug would make it fail.
4. Check whether that bug is realistic and meaningful.
5. Check whether the test controls both the input and the expected output in a tautological way.
6. Check whether mocks are replacing the behavior that should be tested.
7. Check whether the test is coupled to private implementation details.
8. Check whether the same confidence could be gained with fewer or better tests.
9. Classify the test as **Keep**, **Fix**, **Cut**, or **Add**.
10. Recommend concrete changes.

## Classification

Use these labels.

### Keep

The test protects meaningful behavior and would fail on a realistic regression.

A good Keep test usually has at least one of these traits:

- verifies public API behavior
- covers an important branch or edge case
- protects a known regression
- checks error handling or recovery
- exercises integration between components that commonly break
- validates security, permissions, data integrity, or compatibility
- would still be valuable after a harmless refactor

### Fix

The test has a useful intent but weak execution.

Fix when the test is:

- too coupled to implementation details
- over-mocked
- asserting calls instead of outcomes
- missing the important assertion
- using snapshots where targeted assertions would be better
- too broad or too brittle
- not covering the risky branch it claims to cover
- duplicating setup so heavily that the behavior is hard to see
- likely to pass even if the real behavior is broken

### Cut

The test adds little or no bug-finding value.

Cut when the test:

- only asserts constants, fixtures, or mocks
- tests framework or library behavior
- tests a getter, wrapper, or pass-through with no meaningful logic
- only verifies that a mock was called exactly as arranged
- duplicates another stronger test
- snapshots unimportant output
- mirrors the implementation line-for-line
- would fail only on a harmless refactor
- exists mainly for coverage
- has no clear user, caller, or system impact

### Add

Important behavior or risk is untested.

Add tests for:

- known regressions
- boundary conditions
- malformed input
- empty input
- duplicate input
- permission failures
- auth or tenant isolation
- error handling
- retries and partial failure
- time, timezone, ordering, or race conditions
- serialization/deserialization
- persistence behavior
- compatibility across versions or platforms
- security-sensitive behavior
- integration points where mocks hide risk

## Test Smells

Flag these aggressively:

- **Mocking the thing being tested** — the test proves the mock works, not the system.
- **Tautological expectations** — expected value is generated by the same logic as the implementation.
- **Interaction-only testing** — asserts calls but not observable outcome.
- **Snapshot dumping** — huge snapshot with no semantic reason to exist.
- **Coverage padding** — test touches code but proves no important behavior.
- **Private-detail coupling** — harmless refactor breaks the test.
- **Fixture worship** — test mostly verifies test data.
- **Duplicate confidence** — many tests prove the same low-value fact.
- **No-failure-path testing** — only happy path is covered where failure behavior matters.
- **Brittle timing** — sleeps, races, or async behavior not controlled.
- **Overbroad setup** — test intent buried under irrelevant construction.
- **Assertion afterthought** — test has elaborate setup but weak final assertion.
- **Testing library behavior** — proves React, Rails, Jest, SQLAlchemy, etc. work as documented.
- **“Does not throw” only** — acceptable only when no better observable behavior exists.

## Preferred Testing Style

Prefer tests that go through stable public interfaces and assert meaningful outcomes.

In general:

1. Behavior tests beat implementation tests.
2. Integration-style tests beat mock-heavy unit tests when the integration is the risk.
3. Targeted assertions beat giant snapshots.
4. Regression tests beat generic coverage.
5. One strong test beats several shallow tests.
6. Testing the boundary is better than testing every internal helper.
7. A test that fails for the right reason is better than a test that merely increases coverage.

Mock external systems when necessary, but do not mock away the behavior that gives the test value.

## Handling Snapshots

Keep a snapshot only if:

- the output is genuinely important
- the snapshot is reviewed as a meaningful artifact
- small unintended changes should fail the test
- the snapshot is not mostly noise
- targeted assertions would be insufficient or less clear

Otherwise, replace the snapshot with focused assertions or cut it.

## Handling Mocks

Mocks are acceptable when they isolate:

- slow external systems
- nondeterministic services
- network calls
- payment providers
- email/SMS/push providers
- analytics clients
- expensive infrastructure
- failure cases that are hard to trigger otherwise

Mocks are suspicious when they replace:

- the core logic under test
- the only meaningful branch
- the data transformation being verified
- the persistence behavior that could break
- the integration point that the test claims to protect

When a test uses mocks, ask:

> “If the real dependency changed or broke, would this test catch anything useful?”

## Output Structure

Use this structure unless the user requests another format:

```markdown
## Verdict

<Strong, mixed, weak, overfit, under-tested, mostly noise, or high-signal.>

<Brief explanation of the overall test quality and the highest-risk weakness.>

## What These Tests Actually Protect

- <Behavior/risk currently protected>
- <Behavior/risk currently protected>

## Biggest Problems

### 1. <Problem title>

- **Severity:** High / Medium / Low
- **Why it matters:** <Impact on bug-finding value>
- **Example:** <Test/file/name if available>
- **Recommendation:** <Cut, fix, rewrite, or replace>

### 2. <Problem title>

- **Severity:** High / Medium / Low
- **Why it matters:** <Impact on bug-finding value>
- **Example:** <Test/file/name if available>
- **Recommendation:** <Cut, fix, rewrite, or replace>

## Keep

- `<test/file/name>` — <why it earns its place; what bug it would catch>

## Fix

- `<test/file/name>` — <what is weak; how to rewrite it; what bug the rewritten test should catch>

## Cut

- `<test/file/name>` — <why it adds little or no value>

## Add

- <Missing behavior or risk> — <specific test to add and why it matters>

## Highest-Value Next Changes

1. <Most important cut/fix/add>
2. <Next most important cut/fix/add>
3. <Next most important cut/fix/add>

## Bottom Line

<Direct recommendation on whether the current test suite/change is good enough.>
```

## If Asked to Edit Tests

Only modify tests if the user explicitly asks for changes.

When editing:

1. Preserve tests that protect meaningful behavior.
2. Remove tests that do not earn their place.
3. Rewrite weak tests around observable behavior.
4. Add missing regression tests for important risks.
5. Avoid expanding the suite with low-signal coverage.
6. Run or recommend the most relevant test command.
7. Explain what changed and why.

Do not delete tests merely because they are imperfect. Delete them when they are redundant, misleading, brittle, or low-signal compared with their maintenance cost.

## Rules

- Be honest. Do not defend tests just because they exist.
- Do not reward coverage for its own sake.
- Do not require tests for every line, getter, wrapper, or framework integration point.
- Do not confuse “unit test” with “mock everything.”
- Do not confuse “integration test” with “slow and unfocused.”
- Do not accept snapshots unless they verify meaningful output.
- Do not treat private method coverage as inherently valuable.
- Do not ignore missing failure-path coverage.
- Do not overfit recommendations to personal taste; tie every judgment to bug-finding value.
- If a test would still pass after breaking the real behavior, mark it **Fix** or **Cut**.
- If a test would fail only because internal structure changed while behavior stayed correct, mark it **Fix** or **Cut**.
- If the current tests are strong, say so clearly, but still identify the remaining blind spots.

## Quality Bar

A good audit should make clear:

- which tests protect real behavior
- which tests are noise
- which tests are misleading
- which missing tests create risk
- what to cut, fix, and add first

A bad audit merely says “add more tests,” “increase coverage,” or “looks fine” without proving what bugs the tests would catch.