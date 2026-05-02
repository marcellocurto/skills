---
name: test-quality-audit
description: Audit tests for real bug-finding value. Use when the user asks whether tests caught non-obvious bugs, are trivial, are over-mocked, only pass because both sides are controlled, test unnecessary surfaces, or asks to be honest and cut/fix tests that do not earn their place.
---

# Test Quality Audit

Review tests ruthlessly for signal. Keep tests that protect behavior; cut or fix tests that only mirror implementation, assert trivia, or pass because the test controls both sides.

## What to Check

For each test or test group, ask:

- **Bug-finding value**: Would this catch a real bug that is not already obvious from the implementation?
- **Behavior vs implementation**: Does it verify user-visible behavior or public API behavior, not private structure?
- **Trivial pass risk**: Is it testing mocks, fixtures, snapshots, or constants the test itself controls?
- **Coupling**: Would a harmless refactor break it?
- **Surface area**: Is this surface worth testing, or is it framework/library behavior, boilerplate, or a thin pass-through?
- **Missing coverage**: Are important branches, edge cases, failure modes, or regressions untested?

## Audit Method

1. Inspect the implementation enough to understand actual behavior and risk.
2. Inspect the tests and identify what each one would fail on.
3. Classify each test:
   - **Keep** — protects meaningful behavior.
   - **Fix** — valuable intent, weak execution.
   - **Cut** — low signal, redundant, or implementation-coupled.
   - **Add** — missing test for important risk.
4. Recommend concrete changes. If asked to edit code, remove/fix tests that do not earn their place.

## Output Structure

```markdown
## Verdict

<Honest summary: strong, mixed, weak, overfit, or mostly noise.>

## Keep

- <Test/file> — <why it earns its place>

## Fix

- <Test/file> — <what is wrong and how to rewrite it>

## Cut

- <Test/file> — <why it adds little/no value>

## Add

- <Missing behavior/risk> — <test that should exist>

## Highest-Value Next Changes

1. <Most important cut/fix/add>
2. <Next most important change>
```

## Rules

- Be honest; do not defend tests just because they exist.
- Prefer fewer, stronger tests over broad low-signal coverage.
- Do not require tests for every line, getter, wrapper, or framework integration point.
- Integration-style tests through public interfaces usually beat implementation-detail unit tests.
- Mock external systems when necessary, but do not mock the behavior being tested.
- Snapshot tests must prove meaningful output; otherwise cut or replace with targeted assertions.
- If a test would still pass after breaking the real behavior, it must be fixed or cut.
