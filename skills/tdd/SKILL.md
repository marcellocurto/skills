---
name: tdd
description: Build features and bug fixes test-first around meaningful behavior.
---

# Test-Driven Development

TDD is a sequence of small red → green cycles. Each cycle must make the intended behavior executable, demonstrate that the check fails for the intended reason, and make the smallest production change that passes it. The resulting tests must be worth keeping.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Before writing a test, identify the seam under test. Reuse an established public seam when the codebase and nearby tests make it clear. Ask the user only when introducing a new seam, changing the shape of an interface, or choosing among plausible seams would materially change the scope or contract.

Testing effort should land on critical paths and complex logic rather than every edge case.

When the shape of the interface is itself in question—how deep the module is, where the seam belongs, or what the interface should expose—use the `codebase-design` skill for the shared module and seam vocabulary.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Feature cycle

Work in vertical slices:

1. Choose the smallest observable behavior at an established or agreed seam.
2. Write one focused test that specifies that behavior.
3. Run it before changing production code. Confirm that it fails because the behavior is missing, not because the test is broken.
4. Make the smallest production change that passes the test without anticipating later slices.
5. Rerun the test and confirm that it passes.
6. Repeat with the next behavior, allowing each cycle to inform the next.

## Bug-fix cycle

When a bug has a clear, practical regression path:

1. Identify the intended behavior, current behavior, affected path, and smallest observable reproduction.
2. Choose the narrowest executable check already used near that codepath.
3. Add the smallest focused regression test that would have caught the bug.
4. Run it before fixing the implementation. Confirm that it fails for the intended reason; correct the test or reproduction if it passes or fails for an unrelated reason.
5. Make the smallest production change that restores the intended behavior while preserving nearby contracts.
6. Rerun the regression test, then run relevant adjacent tests, type checks, lint, or scenario checks in proportion to the change's risk.

### When a failing test is impractical

Do not create substantial test infrastructure, brittle mocks, slow end-to-end setup, production-only state, or broad fixture churn merely to satisfy the workflow. Prefer no new test over a test with weak or misleading signal.

Before fixing the bug, explain why a durable failing test is not worth its cost and choose the closest meaningful executable regression check. This may be a targeted script, manual reproduction command, browser workflow, log assertion, or focused integration check. The fallback must exercise the broken behavior closely enough to distinguish the fix from the prior failure.

## Guardrails

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- Do not change tests merely to match an incorrect implementation.
- Do not weaken existing assertions unless the intended behavior has genuinely changed and the reason is clear.
- Keep a regression test focused on the reported bug; avoid unrelated coverage expansion or fixture churn.
- If a bug is flaky, make the regression signal deterministic where practical and state what signal is being locked down.
- If a bug exposes a broader class of failures, establish the focused regression path first, then consider sibling coverage.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

## Final response

Report the evidence, not only the outcome:

- Name the failing-before test or executable check and the failure it produced.
- Name the passing-after test run and any nearby validation performed.
- If failing-before evidence could not be demonstrated, state why and describe the closest regression check used instead.
