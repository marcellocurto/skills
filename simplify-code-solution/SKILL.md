---
name: simplify-code-solution
description: Simplify code fixes and feature proposals by grounding them in real requirements and existing code. Use when a coding plan feels overbuilt, speculative, too abstract, or needs assumptions challenged before implementation.
---

# Simplify Code Solution

Find the smallest complete solution to a code problem.

## Goal

Prefer direct, boring changes that meet every real requirement. Simpler is valid only when it preserves behavior, fits existing patterns, and can be verified.

## Success Criteria

- The actual problem and success criteria are explicit.
- Requirements are separated from assumptions and nice-to-haves.
- Relevant code has been inspected before judging the approach.
- Every proposed abstraction, refactor, dependency, or state change is justified by a real requirement.
- The recommendation or implementation is the smallest complete change that preserves behavior and fits local patterns.
- Tradeoffs and validation are stated.

## Constraints

- Reuse existing paths, helpers, types, components, and APIs before adding new ones.
- Avoid rewrites for localized bugs, state machines for simple state, generic frameworks for one caller, speculative migrations, unnecessary dependencies, wide API changes for internal convenience, and tests that only mirror implementation.

## Context Budget

Inspect the minimum relevant code needed to understand the current path, contract, and risk. Continue reading only when a requirement, behavior boundary, local pattern, or validation path is unclear.

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

## Stop Rules

Stop once the smallest complete path is clear and either implemented or recommended with validation. Ask only when the missing information would materially change the solution.
