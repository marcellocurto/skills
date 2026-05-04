---
name: simplify-code-solution
description: Find simple, elegant solutions to code problems by challenging assumptions, grounding proposals in the actual codebase, and choosing the smallest implementation that satisfies the real requirements. Use when the user wants to simplify an overcomplicated fix or feature plan, question implementation assumptions, reduce scope, avoid unnecessary abstractions, or find a pragmatic path for a coding problem without losing required behavior.
---

# Simplify Code Solution

Solve code problems with the least complexity that still meets the requirements.

Use this skill to turn broad, thorough, or over-engineered implementation ideas into a grounded solution that is easy to understand, easy to verify, and consistent with the existing codebase.

## Core Rule

Prefer the simplest complete solution, not the simplest-looking one.

A simpler solution is acceptable only if it:

- satisfies every stated requirement
- preserves important existing behavior
- fits the codebase's current patterns
- has a clear validation path
- avoids shifting complexity into hidden edge cases, manual work, or future maintenance

Do not confuse elegance with cleverness. Favor boring code, direct control flow, local changes, and existing abstractions when they are enough.

## Workflow

1. Restate the real problem in one or two sentences.
2. List the hard requirements separately from assumptions, preferences, and nice-to-haves.
3. Inspect the relevant code before judging implementation shape when repository access is available.
4. Identify the current proposal's complexity sources:
   - new abstractions
   - broad refactors
   - extra state
   - premature generalization
   - unnecessary dependencies
   - new workflows, configs, migrations, or compatibility layers
5. Challenge each complexity source with: "What requirement forces this?"
6. Look for an existing code path, helper, type, component, API, or pattern that already solves most of the problem.
7. Propose the smallest viable change that satisfies the requirements.
8. Name the tradeoffs honestly, including what the simpler path does not solve.
9. Define validation that proves the simple solution works.

If the user asked for implementation, implement the simplest complete fix after this analysis. If the user asked for advice or a plan, stop at the recommended path.

## Simplicity Tests

Before recommending or writing code, test the solution against these questions:

- Can this be solved by changing one existing code path instead of adding a new layer?
- Can the existing data model, API contract, or component boundary stay intact?
- Is a new abstraction justified by repeated real use, or only by imagined future cases?
- Can an edge case be handled locally instead of redesigning the whole flow?
- Is there a smaller behavior-preserving fix that avoids a migration or dependency?
- Would a future maintainer understand the change from the surrounding code?
- Does the validation check user-visible behavior rather than implementation trivia?

If a complex solution survives these questions, keep it. Simplicity is a filter, not a rule against necessary engineering.

## Output Shape

When giving a recommendation, use this structure:

- **Real requirement**: the smallest accurate statement of what must work.
- **Assumptions to drop**: unsupported ideas that made the solution bigger.
- **Simpler path**: the recommended implementation in concrete steps.
- **Tradeoffs**: what this path intentionally does not handle.
- **Validation**: focused tests or manual checks.

Keep the answer direct. Avoid long menus of alternatives unless the requirements are genuinely uncertain.

## Implementation Guidance

When editing code:

- Keep the patch close to the broken or requested behavior.
- Reuse existing project primitives before introducing new ones.
- Prefer deleting special cases over adding more special cases when behavior stays correct.
- Add a helper only when it removes real duplication or clarifies a non-obvious rule.
- Avoid speculative extensibility, framework switches, and broad cleanup.
- Add tests in proportion to risk; prefer one meaningful regression test over many shallow tests.
- If the simple fix depends on an assumption, verify it in code or call it out explicitly.

## Red Flags

Push back when a proposal includes:

- a rewrite to fix a localized bug
- a new state machine for a two-state behavior
- a generic framework for one concrete caller
- a migration before proving the current model cannot work
- a dependency for logic already available in the stack
- wide API changes to satisfy one internal use case
- tests that only mirror the proposed implementation

For each red flag, either remove the complexity or explain the requirement that makes it necessary.
