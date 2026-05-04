---
name: test-quality-audit
description: Audit tests for real bug-finding value. Use when the user asks whether tests are useful, trivial, redundant, over-mocked, implementation-coupled, snapshot-heavy, coverage-padding, only passing because the test controls both sides, or whether tests should be kept, fixed, cut, or added. Also use when reviewing test changes in a PR and the user wants honest judgment about whether the tests earn their place.
---

# Test Quality Audit

Judge tests by signal, not volume.

The core question is: **What realistic bug or regression would this catch?**

If the answer is vague, trivial, controlled by the test, or unrelated to user/caller/system behavior, the test is weak.

## Standard

Keep tests that protect meaningful behavior. Fix or cut tests that mostly prove mocks, fixtures, snapshots, implementation details, or coverage.

Do not ask for more tests by default. Prefer a smaller suite that fails for the right reasons.

## Inspect

Do not audit tests in isolation when code is available. Inspect:

- implementation under test
- public API or user-visible behavior
- important branches and failure paths
- fixtures, mocks, factories, snapshots, helpers
- existing tests for the same behavior
- PR intent, bug report, or known regression when available
- external boundaries: database, API, auth, queue, filesystem, time, randomness, network

## Method

For each test or test group, answer:

1. What behavior does it claim to protect?
2. What behavior does it actually protect?
3. What realistic bug would make it fail?
4. Would that bug matter?
5. Could real behavior break while this still passes?
6. Could a harmless refactor break this?
7. Is this the right level: unit, integration, contract, end-to-end, or none?

## Classify

- **Keep**: protects meaningful behavior and would fail on a realistic regression.
- **Fix**: useful intent, weak execution. Rewrite around observable behavior or the risky boundary.
- **Cut**: little bug-finding value, redundant, tautological, brittle, or coverage-only.
- **Add**: important behavior or risk is untested.

## Smells

Flag tests that:

- mock the thing being tested
- assert calls instead of outcomes
- generate expected values with the same logic as production
- snapshot noisy output without semantic review
- verify fixtures, constants, wrappers, getters, or framework behavior
- duplicate another stronger test
- couple to private structure
- cover only happy paths where failure handling matters
- use sleeps or uncontrolled async timing
- pass even if the real dependency, persistence, or transformation breaks

Snapshots and mocks are acceptable only when they preserve signal. They are bad when they replace the behavior the test claims to verify.

## Output

Use concise Markdown:

- **Verdict**: high-signal, mixed, weak, overfit, under-tested, mostly noise, or good enough.
- **What is protected**: meaningful behavior currently covered.
- **Biggest problems**: prioritized issues with examples and recommendations.
- **Keep / Fix / Cut / Add**: concrete classifications.
- **Highest-value next changes**: the smallest set of edits that improves confidence.
- **Bottom line**: whether the tests earn their place.

## If Asked to Edit Tests

Only modify tests when the user explicitly asks.

When editing:

- preserve high-signal tests
- rewrite weak tests around observable behavior
- remove tests that are redundant, misleading, brittle, or low-signal
- add focused regression coverage for important risks
- run or recommend the most relevant test command

## Rules

- Be honest; do not defend tests because they exist.
- Tie every judgment to bug-finding value.
- Do not reward coverage for its own sake.
- Do not require tests for every line or helper.
- Do not confuse unit tests with mocking everything.
- If the tests are strong, say so and name the remaining blind spots.
