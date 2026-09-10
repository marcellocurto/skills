---
name: test-quality-audit
description: Judge whether tests catch realistic regressions and recommend what to keep, change, or remove.
---

# Test Quality Audit

Judge tests by signal, not volume.

The core question is: **What realistic bug or regression would this catch?**

Call a test weak only when evidence shows that its signal does not protect a meaningful contract or justify its maintenance cost. If missing context prevents that judgment, state the uncertainty rather than assuming the test has little value.

## Goal

Identify the contracts and realistic regressions tests protect, and where their assertions, isolation, or duplication provide misleading evidence or unnecessary maintenance cost.

Do not ask for more tests by default. Prefer a smaller suite that fails for the right reasons.

## Success Criteria

- Each judgment is tied to realistic bug-finding value.
- Meaningful behavior currently protected by the tests is identified.
- Weak, redundant, tautological, brittle, or overfit tests are named concretely.
- Recommendations classify tests as **Keep**, **Fix**, **Cut**, or **Add**.
- The highest-value next changes are small and behavior-oriented.

## Context Budget

Do not audit tests in isolation when code is available. Start with the tests under review, then inspect only the code and nearby tests needed to judge signal:

- implementation under test
- public API or user-visible behavior
- important branches and failure paths
- fixtures, mocks, factories, snapshots, helpers
- existing tests for the same behavior
- PR intent, bug report, or known regression when available
- relevant test changes and the commands, selection rules, and prerequisites that determine whether those tests run
- external boundaries: database, API, auth, queue, filesystem, time, randomness, network

Use the minimum code and test context needed to judge signal. Continue reading only when a test’s claimed behavior, real dependency, risky branch, or nearby stronger coverage is unclear.

## Method

For each test or test group, answer:

1. What behavior does it claim to protect?
2. What behavior does it actually protect?
3. What realistic bug would make it fail?
4. Would that bug matter?
5. Could real behavior break while this still passes?
6. Could a harmless refactor break this?
7. Is this the right level: unit, integration, contract, end-to-end, or none?
8. Did the claimed validation actually run this test under the relevant conditions?

When tests changed, compare the protected behavior before and after: what realistic failure would the previous test catch that the replacement now accepts? Inspect changed assertions, fixtures, mocks, snapshots, skips, and configuration together. Establish whether lost protection follows an authorized contract change or a demonstrated error in the old test. A changed interface alone does not authorize dropping its failure cases.

For an important claim whose sensitivity is uncertain, use existing failing-before evidence or a focused check against a known broken version when practical. If a temporary defect would resolve that uncertainty, use an isolated disposable copy, preserve the test, restore the copy afterward, and report the observation. Do not mutate the reviewed checkout or require broad mutation infrastructure. A passing result against the defect disproves only the protection that experiment exercised.

## Classify

- **Keep**: protects meaningful behavior and would fail on a realistic regression.
- **Fix**: useful intent, weak execution. Rewrite around observable behavior or the risky boundary.
- **Cut**: little bug-finding value, redundant, tautological, brittle, or coverage-only.
- **Add**: important behavior or risk is untested.

## Investigate signals

Treat test patterns as leads, not verdicts. Establish the contract, the realistic regression the test catches or misses, and any concrete maintenance cost before recommending a change:

- **Call, count, and ordering assertions:** useful when an interaction is part of the contract, such as dispatching one message for duplicate submissions or following a required protocol sequence. Investigate whether the assertion instead freezes private helper calls while the promised outcome could still fail.
- **Constants and fixtures:** can provide independent expectations for published formats, protocol values, or compatibility requirements. Distinguish those checks from assertions that compare fixture-controlled values with themselves or merely repeat non-critical configuration. Judge wrappers and getters by the behavior they own, not their size or name.
- **Snapshots:** can protect a stable, meaningful output contract when changes receive semantic review. Investigate noisy incidental output, unnoticed contract changes, or bulk snapshot updates that accept a regression. Snapshot syntax alone does not make a test weak.
- **Mocks and other doubles:** can isolate a meaningful contract or control failure conditions. Check whether they replace the behavior under test or conceal broken wiring, persistence, or transformation that the test claims to verify.
- **Setup and capability selection:** check whether fixtures initialize state, enable features, or supply configuration that the supported workflow does not guarantee. Keep tests of valid prepared states, but do not credit them as proof of readiness or availability. Error-handling tests can be valuable while successful use remains untested or broken.
- **Execution gaps:** inspect opt-ins, skips, expected-failure markers, and required infrastructure. A suite excluded from the actual validation command cannot support its success claim. Recommend required deterministic coverage in the required command, with visible failure for unavailable prerequisites; keep optional live-service checks explicit.
- **Calculated expectations:** check whether the oracle is independent of the implementation. Repeating the same flawed calculation can hide a bug; a computed expectation grounded independently in the contract is not automatically tautological.
- **Overlapping or internal tests:** compare what the tests check before calling them redundant or tied to implementation details. Keep internal tests when they catch important failures that other tests would miss. Flag assertions on private structure when harmless refactors break them or real regressions still pass.
- **Tests using an old API:** check whether a replaced production API or adapter remains only because tests still use it. Find other callers and check compatibility requirements before recommending removal. If the old API is no longer needed, classify useful tests as **Fix** and recommend updating them to use the replacement while checking the same behavior. An internal API used only by tests may still protect useful behavior; that alone is not a reason to remove it or its tests.
- **Failure and timing coverage:** examine missing failure paths, sleeps, or uncontrolled timing when they can hide a realistic defect or make results unreliable. Do not demand every edge case merely because it exists.

Keep a pattern when it provides useful evidence for the stated contract. Recommend a change only after establishing the weakness, rather than requiring the author to defend a pattern merely because it appears on this list.

## Output

Lead with the verdict and highest-value changes. Keep the evidence needed to justify each classification; omit repeated test summaries and generic testing advice.

Group repeated weaknesses by the mechanism that loses signal or adds maintenance cost. Cite representative examples and identify the affected test groups. Preserve separate classifications when their contracts or evidence differ; shared syntax alone is not a reason to merge findings.

Use only the sections that add information:

- **Verdict**: high-signal, mixed, weak, overfit, under-tested, mostly noise, or good enough.
- **What is protected**: meaningful behavior currently covered.
- **Biggest problems**: prioritized issues with examples and recommendations.
- **Keep / Fix / Cut / Add**: concrete classifications.
- **Highest-value next changes**: the smallest set of edits that improves confidence.

## If Asked to Edit Tests

Only modify tests when the user explicitly asks.

When editing:

- preserve high-signal tests
- rewrite weak tests around observable behavior
- remove tests that are redundant, misleading, brittle, or low-signal
- add focused regression coverage for important risks
- run the most relevant test command when available; otherwise explain the next best check

Derive expectation changes from authorized requirements or evidence that the old test was wrong. Preserve meaningful cases when adapting interfaces or setup. If a corrected test exposes a production defect outside the authorized edit, leave it failing and report the defect; test cleanup does not authorize a production fix or weakening the expectation. State passed, failed, skipped, and unable-to-run outcomes separately.

## Constraints

- Be honest; do not defend tests because they exist.
- Tie every judgment to bug-finding value.
- Do not reward coverage for its own sake.
- Do not require tests for every line or helper.
- Do not confuse unit tests with mocking everything.
- If the tests are strong, say so and name the remaining blind spots.

## Stop Rules

Stop when the audit explains what real bugs the tests would catch, what could still break, and the smallest useful improvement. Ask only when missing context prevents judging the tests’ behavior.
