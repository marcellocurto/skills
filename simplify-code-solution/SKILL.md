---
name: simplify-code-solution
description: Simplify code fixes and feature proposals by grounding them in real requirements and existing code. Use when a coding plan feels overbuilt, speculative, too abstract, or needs assumptions challenged before implementation.
---

# Simplify Code Solution

Find the smallest complete solution to a code problem.

## Principle

Prefer direct, boring changes that meet every real requirement. Simpler is valid only when it preserves behavior, fits existing patterns, and can be verified.

## Workflow

1. Define the actual problem and success criteria.
2. Separate requirements from assumptions and nice-to-haves.
3. Inspect relevant code before judging the approach.
4. For each abstraction, refactor, dependency, or state change, ask: "What requirement forces this?"
5. Reuse existing paths, helpers, types, components, and APIs before adding new ones.
6. Recommend or implement the smallest change that works.
7. State tradeoffs and validation.

## Simplicity Checks

- Can one existing code path change instead of adding a layer?
- Can current contracts and data shapes remain unchanged?
- Is the abstraction serving repeated real use, not imagined future use?
- Can the edge case be handled locally?
- Will a maintainer understand it from nearby code?
- Does validation cover behavior users or callers rely on?

## Output

For recommendations:

- **Real requirement**
- **Assumptions to drop**
- **Simpler path**
- **Tradeoffs**
- **Validation**

For implementation, make the scoped change and verify it.

## Avoid

- rewrites for localized bugs
- state machines for simple state
- generic frameworks for one caller
- migrations before proving the current model fails
- dependencies for logic the stack already has
- wide API changes for internal convenience
- tests that only mirror implementation
