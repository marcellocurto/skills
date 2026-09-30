---
name: simplify-code-solution
description: Simplify a proposed or existing code solution through recommendations or implementation while preserving requirements and clear ownership.
---

# Simplify Code Solution

Find the simplest complete production design for a code problem, whether it is a proposed solution or existing code. Simpler means easier to understand and change while keeping every real requirement. Fewer files, functions, or lines do not by themselves make a solution simpler.

## 1. Choose the mode

- **Recommend:** for questions such as "Could this be simpler?" or a review of a proposal. Do not edit files. A request to revise a proposal changes the proposal, not the code it describes.
- **Implement:** when the user asks to simplify or refactor the code, or to apply a recommendation. Make the change and verify it without asking for approval again.

Stay in recommend mode unless the user asked for changes; liking a design is not a request to implement it. Ask only when a missing decision would change the solution or its scope.

## 2. Understand what the code must do

Read the code on the current path, its callers, its tests, and the local patterns, and stop reading once the requirements and risks are clear. Then separate:

- **Requirements:** the behavior and contracts callers rely on, and the success criteria.
- **Assumptions and nice-to-haves** that could be dropped.
- **Complexity to keep:** code that encodes real domain rules, durability, recovery, or operational guarantees. Durable queues, explicit state, and domain distinctions often look heavy and are still needed.

Before proposing to remove a mechanism, know its consumers, its role in operation and failure handling, and what would replace it.

## 3. Find the simpler shape

Look for:

- an existing path, helper, type, component, or API that can absorb the behavior without taking on an unrelated responsibility
- code that duplicates what the language, framework, or an existing dependency already provides
- generic code, extension points, or configuration with only one real variation
- rewrites for localized bugs, state machines for simple state, frameworks for one caller, speculative migrations, new dependencies, or wide API changes for internal convenience
- wrappers that only add a call to follow; read their callers first, and keep wrappers that handle rules, cleanup, or compatibility the callers would otherwise carry
- logic placed away from its natural owner, or an owner that has taken on an independent workflow

A focused module is justified, even with one caller, when it hides real complexity and reduces what callers must know. Compare total lifecycle cost, not initial size, and reject a simplification that moves complexity, risk, or manual work downstream.

When replacing an interface, find every user, including tests. Move tests to the replacement while checking the same behavior; do not keep an old API only for tests. Keep it while other callers or a rollout need it, and say when a temporary adapter can be removed.

When you find a simplification, check the rest of the requested scope for the same problem and include those cases. Report cases outside the scope separately.

## 4. Implement

In implement mode, run the relevant tests before the refactor and keep the same meaningful cases afterward. Change an expected outcome only for an authorized contract change or a demonstrated error in the test. Do not change fixtures, mocks, or test selection in ways that hide a failure. If the work includes a behavior fix, use the `tdd` skill when available; otherwise, watch the regression test fail before fixing the code.

Continue through the change and its verification; do not stop at a proposal. If a blocker stops you, keep any valid failing test and report the missing decision and what remains.

## 5. Report

For a recommendation, use this format and omit lines that add nothing:

```markdown
**Requirements:** what the code must keep doing.

**Complexity to keep:** what stays, and why.

**Assumptions to drop:** what the current design assumes without a requirement.

**Simpler path:** the concrete change, with locations.

**Tradeoffs:** what gets worse or riskier.

**Validation:** how to confirm behavior is preserved.
```

For an implementation, report what changed, why it is simpler, the checks run with their results, and any limitation.
