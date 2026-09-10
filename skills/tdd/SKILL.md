---
name: tdd
description: Build features and bug fixes test-first around meaningful behavior.
---

# Test-Driven Development

TDD is a sequence of small red → green → refactor cycles. Make the intended behavior executable and observe its failure before implementing it. A completed cycle leaves the affected path in a production-quality shape; a blocked cycle preserves the valid failing test and reports what prevents completion.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests protect a meaningful contract through an interface or observation that can detect a realistic regression. Prefer tests that survive implementation-only refactors of that contract. A test such as "user can checkout with valid cart" explains the capability it protects; changing the contract itself may legitimately require changing its tests.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is a boundary where a test exercises behavior or controls a dependency. It may be a public API or an internal interface owned by a module. An internal module can have its own contract and meaningful tests without exposing that interface to application callers. Do not bypass encapsulation merely to assert on incidental private state.

Before writing a test, identify the requirement that establishes the expected outcome, the starting conditions, and the realistic failure it should catch. Then choose where to call the code or control its dependencies. Prefer existing interfaces and nearby test conventions. Use an internal interface when its tests catch important failures that other tests would miss. Do not expose private state or add an abstraction just to make a test easier to write. Ask only when the choice would change the agreed scope or a contract.

Testing effort should land on critical paths and complex logic rather than every edge case.

When the shape of the interface is itself in question—how deep the module is, where the seam belongs, or what the interface should expose—use the `codebase-design` skill for the shared module and seam vocabulary.

## Anti-patterns

- **Implementation-coupled**: asserts incidental private state, helper calls, or ordering that the tested contract does not promise. Internal tests, collaborator doubles, and direct database observations are not inherently coupled; judge whether they detect a real contract failure or merely freeze the implementation's shape.
- **Tautological or non-independent expectations**: an assertion that derives its expected value from the result under test cannot provide independent evidence. Copying production logic into the expected-value calculation can also reproduce the same bug. Use expectations grounded independently in the contract, a worked example, or a trusted oracle; a calculated expectation is not automatically tautological.
- **Writing all tests before any implementation:** this can commit the tests to a design before trying it in working code. Write one test, implement its behavior, and use what you learn to choose the next test.

## Feature cycle

Work in vertical slices:

1. Choose the smallest observable behavior at an established or agreed seam.
2. Write one focused test that specifies that behavior.
3. Run it before changing production code. Confirm that it fails because the behavior is missing, not because the test is broken.
4. Make the simplest production-quality change that passes the test without adding future behavior. Extract a focused module when it makes responsibilities clearer, even if it has only one caller.
5. Rerun the test and confirm that it passes.
6. Refactor the affected path when needed to preserve clear ownership and cohesion, then confirm the test still passes.
7. Repeat with the next behavior, allowing each cycle to inform the next.

## Bug-fix cycle

When a bug has a clear, practical regression path:

1. Identify the intended behavior, current behavior, affected path, and smallest observable reproduction.
2. Choose the narrowest executable check already used near that codepath.
3. Add the smallest focused regression test that would have caught the bug.
4. Run it before fixing the implementation. Confirm that it fails for the intended reason; correct the test or reproduction if it passes or fails for an unrelated reason.
5. Make a focused production-quality change that restores the intended behavior while preserving nearby contracts and clear ownership.
6. Rerun the regression test, then run relevant adjacent tests, type checks, lint, or scenario checks in proportion to the change's risk.

## When a failing test is impractical

Do not create substantial test infrastructure, brittle mocks, slow end-to-end setup, production-only state, or broad fixture churn merely to satisfy the workflow. Prefer no new test over a test with weak or misleading signal.

Before implementing the behavior, explain the concrete limitation and choose a check that can demonstrate the missing behavior and its correction. This may be a script, manual command, browser workflow, log assertion, or integration check. It must exercise the required behavior, not merely nearby code that already works. If execution is unavailable, report the evidence gap; do not substitute a test that bypasses it.

A test added after implementation can protect against a regression, but is not evidence of test-first work. If it already passes, inspect whether the behavior exists or the check misses it. Do not manufacture a failure just to claim a red phase. Running a later regression against the old implementation can establish sensitivity; report that sequence accurately.

## Preserve the expectation

Change a test only when the authorized requirement changed, evidence shows the test was wrong against that requirement, or an interface/setup change preserves the same protected behavior. State the reason for a material expectation change. The implementation's new output is not authority to change its expected output.

This applies to assertions, fixtures, mocks, snapshots, skips, expected-failure markers, and test selection. Do not make a failing case pass by removing its relevant starting conditions, accepting its error as success, or bypassing the failing collaborator. When replacing a test, retain its meaningful failure cases unless their contract was explicitly retired.

Distinguish a test defect, unavailable execution, and a real contract failure. Fix a broken reproduction without changing the intended outcome. A setup or infrastructure error is not the required behavioral red; preserve and report it separately if it prevents reaching that behavior.

## When green is blocked

Continue authorized implementation and necessary restructuring while they can satisfy the expectation. Refactoring after green does not prohibit structural changes needed to reach green.

If a valid failure requires an unresolved domain decision, unavailable prerequisite, or material scope expansion, preserve the failing test and completed work. Report the expected and actual behavior, the command and failure observed, and the smallest prerequisite or decision needed. Continue independent in-scope work where useful. Do not weaken the test or disable the feature to make validation pass.

A pre-existing defect can still block the requested behavior; its age does not make acceptance optional. A blocked implementation is unfinished. A request only to reproduce a bug or add a failing regression can be complete with that test still red; it does not authorize fixing production code.

## Validation cadence

Within each red → green → refactor cycle, run the focused check and any adjacent checks affected by the current change. Run broader validation when a shared contract, integration risk, failure, or repository rule makes it necessary, not automatically after every slice.

At completion, satisfy applicable repository checks and meaningful regression coverage. Reuse results that still cover the final implementation and relevant conditions; rerun only invalidated or failed checks unless a repository rule requires otherwise. Do not repeat a full suite, build, or lint pass merely to mark another cycle complete.

Verify that the relevant tests actually ran under the reported command. Report passed, failed, skipped, and unable-to-run checks distinctly. Required coverage hidden behind an opt-in or missing prerequisite remains a verification gap, even when the command exits successfully.

## Guardrails

- **Red before green.** Write the failing test first, then implement the current behavior completely. Don't anticipate future tests or add speculative features.
- **One behavior at a time.** Keep each cycle focused on one coherent contract change. Use the observations and dependency controls needed to prove it without batching unrelated behavior into the same cycle.
- Keep a regression test focused on the reported bug; avoid unrelated coverage expansion or fixture churn.
- If a bug is flaky, make the regression signal deterministic where practical and state what signal is being locked down.
- If a bug exposes a broader class of failures, establish the focused regression path first, then consider sibling coverage.
- **Refactor after green when the changed path needs it.** Preserve clear ownership and cohesion before starting the next slice. Keep the refactor within the affected behavior; do not turn the cycle into unrelated cleanup.

## Final response

Report the evidence, not only the outcome:

- Name the failing-before test or executable check and the failure it produced.
- Name the passing-after test run, or the still-failing regression and blocker, with any nearby validation performed.
- If failing-before evidence could not be demonstrated, state why and describe the closest regression check used instead.
