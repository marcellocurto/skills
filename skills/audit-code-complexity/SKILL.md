---
name: audit-code-complexity
description: Find needless code complexity and suggest simpler designs that preserve behavior.
---

# Audit Code Complexity

Find code that is harder to understand, change, or verify than the problem requires, and propose simpler shapes that keep its behavior. Simpler means easier to understand and change while keeping every real requirement; fewer files, functions, or lines do not by themselves make code simpler. This is an audit: do not edit code unless the user asks.

## 1. Set the scope

- **Current state:** audit the named code as it exists, whenever its complexity was introduced.
- **Change:** audit only complexity that the named commits, branch, or pull request introduced or made worse. Read surrounding code for context.
- **Proposal:** audit a design or code the user proposes before it is built, against the requirements it states. A request to revise the proposal changes the proposal, not the code it describes.

Use the change scope only when the user names a change; uncommitted work in the repository is not a reason to switch. If the user asks for both, report them separately.

For a large target, split it by module across parallel read-only subagents where available, and verify their findings yourself before reporting.

## 2. Look for complexity

Read the target, the repository instructions, the callers, the tests, and the configuration, plus only the docs needed to understand required behavior. Use `git log` to see which files change most often; complexity there costs the most. Separate the behavior and contracts callers rely on from assumptions and nice-to-haves nobody asked for; dropping behavior that callers or users could notice is the user's decision, so recommend it rather than assume it.

Look for:

- indirection, wrappers, generic code, extension points, dependencies, or infrastructure that no current requirement needs
- code that duplicates what the language, framework, an existing dependency, or an existing path, helper, type, or API already provides
- rewrites for localized bugs, state machines for simple state, frameworks for one caller, speculative migrations, or wide API changes for internal convenience
- tangled control flow, flag combinations, implicit state, and types that permit invalid states
- the same fact stored or computed in several places
- behavior placed with the wrong owner, such as an entry point or controller holding business rules, or one module mixing unrelated responsibilities
- one change requiring edits across many files, or callers needing to know details the callee should hide
- hidden side effects, broad mutation, misleading names, and dense or clever expressions
- guards, fallbacks, compatibility paths, and code that nothing uses anymore
- an old API kept only because tests still call it
- test setup, helpers, or mocks that hide behavior, encode policy in several places, or force indirection into production code

Before recommending that a wrapper be removed, read its callers, including tests. Keep it if it owns real behavior or protects a contract. If it only forwards a call, suggest moving that call into the module that owns it.

Before calling code unused, search for consumers by symbol and by literal string, including generated code, configuration, reflection, other packages, and scripts. A search with no results is evidence, not proof; say where you looked.

Before proposing to remove a mechanism, know its consumers, its role in operation and failure handling, and what would replace it. Durable queues, explicit state, retries, and domain distinctions often look heavy and are still needed.

When you confirm a problem, check the rest of the target for the same problem and report the locations together. If you inspected only part of the target, say which part.

## 3. Keep only real findings

Report a finding only when all of these hold:

1. It has a concrete cost: the code is harder to understand, change, or test, or it risks bugs or operational problems.
2. Code, usage, tests, or requirements support the claim.
3. A specific simpler alternative preserves the required behavior and contracts.
4. The benefit outweighs the migration and regression risk, and the alternative does not move complexity, risk, or manual work into callers or operations.

Line count, nesting depth, complexity metrics, and unfamiliarity are clues, not findings. Similar-looking code justifies a shared abstraction only when it represents one concept. Skip anything a formatter or linter enforces.

Prefer local changes, but recommend a larger restructuring when the evidence shows it removes much more complexity than local fixes would, and state its migration cost. Every alternative must preserve domain distinctions, data semantics, identity, validation, security, accessibility, compatibility, and durability, recovery, and operational guarantees.

A bug, security issue, or performance problem belongs in this report only when the complexity causes or hides it; label it separately. Tests are in scope only as a source of complexity. For test value and coverage, use the `test-quality-audit` skill.

When replacing an interface, find every user, including tests, and move tests to the replacement while checking the same behavior; do not keep an old API only for tests. Keep it while other callers or a rollout need it, and say when a temporary adapter can be removed.

## Applying a finding

Edit code only when the user asks for it, then carry the change through and verify it without asking again. Run the relevant tests before the refactor and keep the same protected cases afterward. Change an expected outcome only for an authorized contract change or a demonstrated error in the test, and do not change fixtures, mocks, or test selection in ways that hide a failure. If the work includes a behavior fix, use the `tdd` skill when available. If a blocker stops you, keep any valid failing test and report the missing decision and what remains.

## 4. Report

Use this format, order findings by benefit relative to risk, and omit empty sections:

```markdown
**Verdict:** Needs simplification | Minor opportunities | No material findings. One sentence on why.

**Scope:** what was inspected, and what was not.

### 1. Short title

`path/to/file.ts:42`, plus other locations with the same problem.

- **Cost:** what is harder, and the evidence.
- **Simpler shape:** the concrete alternative.
- **Keep:** behavior and contracts that must not change.
- **Risk:** migration and regression risk, and how to verify the change.

**Justified complexity:** complex-looking code that earns its place, only when a reader would likely question it.

**Order:** which findings to do first, only when the order matters.
```
