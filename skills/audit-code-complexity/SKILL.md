---
name: audit-code-complexity
description: Find needless code complexity and suggest simpler designs that preserve behavior.
---

# Audit Code Complexity

Find code that is harder to understand, change, or verify than the problem requires, and propose simpler shapes that keep its behavior. This is an audit: do not edit code unless the user asks.

## 1. Set the scope

- **Current state:** audit the named code as it exists, whenever its complexity was introduced.
- **Change:** audit only complexity that the named commits, branch, or pull request introduced or made worse. Read surrounding code for context.

Use the change scope only when the user names a change; uncommitted work in the repository is not a reason to switch. If the user asks for both, report them separately.

For a large target, split it by module across parallel read-only subagents where available, and verify their findings yourself before reporting.

## 2. Look for complexity

Read the target, the repository instructions, the callers, the tests, and the configuration, plus only the docs needed to understand required behavior. Use `git log` to see which files change most often; complexity there costs the most.

Look for:

- indirection, wrappers, generic code, extension points, dependencies, or infrastructure that no current requirement needs
- tangled control flow, flag combinations, implicit state, and types that permit invalid states
- the same fact stored or computed in several places
- behavior placed with the wrong owner, such as an entry point or controller holding business rules, or one module mixing unrelated responsibilities
- one change requiring edits across many files, or callers needing to know details the callee should hide
- hidden side effects, broad mutation, misleading names, and dense or clever expressions
- guards, fallbacks, compatibility paths, and code that nothing uses anymore
- an old API kept only because tests still call it
- test setup, helpers, or mocks that hide behavior, encode policy in several places, or force indirection into production code

Before recommending that a wrapper be removed, read its callers, including tests. Keep it if it owns real behavior or protects a contract. If it only forwards a call, suggest moving that call into the module that owns it.

When you confirm a problem, check the rest of the target for the same problem and report the locations together. If you inspected only part of the target, say which part.

## 3. Keep only real findings

Report a finding only when all of these hold:

1. It has a concrete cost: the code is harder to understand, change, or test, or it risks bugs or operational problems.
2. Code, usage, tests, or requirements support the claim.
3. A specific simpler alternative preserves the required behavior and contracts.
4. The benefit outweighs the migration and regression risk.

Line count, nesting depth, complexity metrics, and unfamiliarity are clues, not findings. Similar-looking code justifies a shared abstraction only when it represents one concept. Skip anything a formatter or linter enforces.

Prefer local changes, but recommend a larger restructuring when the evidence shows it removes much more complexity than local fixes would, and state its migration cost. Every alternative must preserve domain distinctions, data semantics, identity, validation, security, accessibility, and compatibility.

A bug, security issue, or performance problem belongs in this report only when the complexity causes or hides it; label it separately. Tests are in scope only as a source of complexity. For test value and coverage, use the `test-quality-audit` skill.

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
