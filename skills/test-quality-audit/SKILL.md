---
name: test-quality-audit
description: Judge whether tests catch realistic regressions and recommend what to keep, change, or remove.
---

# Test Quality Audit

A test earns its place by failing on a realistic regression of a contract: behavior that users or callers rely on. Judge every test by that standard, not by coverage, count, or how it was written. Prefer a smaller suite that fails for the right reasons, and do not ask for more tests by default.

Call a test weak only when the evidence shows it protects no contract or costs more to maintain than it protects. If missing context prevents that judgment, say so instead of assuming the test has little value.

## What to read

Start with the tests under review, then read only what you need to judge them:

- the implementation under test and its public or user-visible behavior
- important branches and failure paths
- fixtures, mocks, factories, snapshots, and helpers
- existing tests for the same behavior
- the PR intent, bug report, or known regression when available
- the commands, selection rules, and prerequisites that decide whether the tests run
- external boundaries: database, API, auth, queue, filesystem, time, randomness, network

Keep reading only while a test's claimed behavior, a real dependency, a risky branch, or nearby stronger coverage is unclear.

## Method

For each test or group of tests, answer:

1. What contract does it claim to protect?
2. What does it actually protect?
3. What realistic regression would make it fail, and would that regression matter?
4. Could the contract break while the test still passes?
5. Could a harmless refactor break it?
6. Is the only realistic failure reverting the change that introduced it? If so, it documents a commit, not a contract.
7. Is it at the right level: unit, integration, contract, end-to-end, or none?
8. Did the claimed validation actually run it under the relevant conditions?

### Changed tests

Compare what the tests protected before and after the change: which realistic regression did the old test catch that the new one accepts? Read changed assertions, fixtures, mocks, snapshots, skips, and configuration together. Lost protection is acceptable only when the contract changed by decision or the old test was shown to be wrong. A changed interface alone does not justify dropping its failure cases.

When behavior is removed, the tests deleted with it are not lost protection. Check that the remaining suite still covers what depended on the removed area, and do not recommend tests of absence as replacements.

### Checking sensitivity

When it is unclear whether an important test would fail on the regression it claims to catch, use existing failing-before evidence or run it against a known broken version. If introducing a temporary defect would settle the question, do it in a disposable copy, keep the test unchanged, restore the copy, and report what you saw. Do not modify the reviewed checkout or require mutation-testing infrastructure. A test that passes against a defect is disproved only for that defect.

## Classify

- **Keep**: protects a contract and fails on a realistic regression.
- **Fix**: useful intent, weak execution. Rewrite it around observable behavior or the risky boundary.
- **Cut**: protects no contract. Includes redundant, tautological, brittle, and coverage-only tests, and tests of static content, copy, navigation structure, or non-critical configuration that encode no compatibility promise.
- **Add**: a contract is untested and a realistic regression is plausible. Do not recommend Add for removals, design exploration, prototypes, static content, copy, or configuration.

## Patterns to investigate

These patterns are leads, not verdicts. Establish the contract, the regression the test catches or misses, and the concrete maintenance cost before recommending a change. Keep a pattern that gives useful evidence for its contract.

- **Absence assertions.** A test that a feature, route, option, menu entry, or default no longer exists protects no contract. Cut it. Keep an absence test only when the absence is itself promised, such as an endpoint being unreachable without authentication or a destructive action being off by default.
- **Call, count, and ordering assertions.** Keep them when the interaction is the contract, such as sending exactly one message for duplicate submissions or following a required protocol sequence. Cut or fix them when they freeze private helper calls while the promised outcome could still fail.
- **Constants and fixtures.** Keep checks of published formats, protocol values, and compatibility requirements. Cut assertions that compare fixture-controlled values with themselves or repeat non-critical configuration. Judge wrappers and getters by the behavior they own, not by their size or name.
- **Snapshots.** Keep them when they protect a stable, meaningful output and changes get semantic review. Investigate noisy incidental output, contract changes nobody noticed, and bulk snapshot updates that accept a regression. Snapshot syntax alone is not a weakness.
- **Mocks and other doubles.** Keep them when they isolate a contract or control a failure condition. Flag them when they replace the behavior under test or hide broken integration, persistence, or transformation that the test claims to verify.
- **Setup and capability selection.** Flag fixtures that initialize state, enable features, or supply configuration that the supported workflow does not guarantee. Tests of a valid prepared state can stay, but they do not prove readiness or availability. A suite can test error handling thoroughly while the successful path is untested or broken.
- **Execution gaps.** Inspect opt-ins, skips, expected-failure markers, and required infrastructure. A suite that the validation command does not run cannot support a success claim. Recommend that required deterministic tests run in the required command and fail visibly when a prerequisite is missing; keep optional live-service checks explicit.
- **Calculated expectations.** Check that the expected value is derived independently of the implementation. Repeating the implementation's calculation hides its bugs; an expectation grounded in the contract is not tautological merely because it is computed.
- **Overlapping or internal tests.** Compare what the tests check before calling them redundant or implementation-bound. Keep internal tests that catch important failures other tests miss. Flag assertions on private structure when harmless refactors break them or real regressions still pass.
- **Tests on an old API.** Check whether a replaced production API or adapter survives only because tests still use it. Find other callers and compatibility requirements before recommending removal. If the old API is no longer needed, classify useful tests as Fix and move them to the replacement while checking the same behavior. An internal API used only by tests may still protect useful behavior; that alone is not a reason to remove it or its tests.
- **Failure and timing coverage.** Flag missing failure paths, sleeps, and uncontrolled timing when they can hide a realistic defect or make results unreliable. Do not demand every edge case because it exists.

## Output

Lead with the verdict and the highest-value changes. Keep only the evidence that justifies each classification; leave out repeated test summaries and generic testing advice.

Group repeated weaknesses by the mechanism that loses protection or adds maintenance cost, with representative examples and the affected test groups. Keep classifications separate when their contracts or evidence differ; shared syntax is not a reason to merge findings.

Use only the sections that add information:

- **Verdict**: strong, mixed, weak, overfit, under-tested, mostly noise, or good enough.
- **What is protected**: contracts the tests currently cover.
- **Biggest problems**: prioritized issues with examples and recommendations.
- **Keep / Fix / Cut / Add**: concrete classifications.
- **Highest-value next changes**: the smallest set of edits that improves confidence.

If the tests are strong, say so and name the remaining blind spots. Ask only when missing context prevents judging what a test protects.

## Editing tests

Edit tests only when the user explicitly asks. When editing, preserve tests that protect contracts, rewrite weak tests around observable behavior, remove tests that are redundant, misleading, brittle, or protect no contract, and add focused regression tests for important risks. Run the most relevant test command when available; otherwise explain the next best check.

Change an expectation only when the requirement changed or the old test was shown to be wrong. Preserve the protected cases when adapting interfaces or setup. If a corrected test exposes a production defect, leave it failing and report it; test cleanup does not authorize a production fix or a weakened expectation. Report passed, failed, skipped, and unable-to-run outcomes separately.

## Constraints

- Do not defend a test because it exists, and do not credit it for having been written first. Test-first process says how the work was done, not what the test protects.
- Do not reward coverage, require a test for every line or helper, or treat unit testing as mocking everything.
