---
name: simplify-code-solution
description: Simplify overbuilt or speculative code fixes and feature proposals by grounding them in real requirements and existing code. Use before implementation when a coding plan needs the smallest complete solution.
---

# Simplify Code Solution

Find the smallest complete solution to a code problem.

## Goal

Prefer direct, boring changes that meet every real requirement. Simpler is valid only when it preserves behavior, fits existing patterns, and can be verified.

## Success Criteria

- The actual problem and success criteria are explicit.
- Requirements are separated from assumptions and nice-to-haves.
- Relevant code has been inspected before judging the approach.
- Essential complexity that represents real domain, durability, recovery, or operational requirements is identified and preserved.
- Every proposed abstraction, refactor, dependency, or state change is justified by a real requirement.
- The recommendation or implementation is the smallest complete change that preserves behavior and fits local patterns.
- Tradeoffs and validation are stated.

## Constraints

- Reuse existing paths, helpers, types, components, and APIs before adding new ones.
- Avoid rewrites for localized bugs, state machines for simple state, generic frameworks for one caller, speculative migrations, unnecessary dependencies, wide API changes for internal convenience, and tests that only mirror implementation.
- Complexity is not a defect merely because it is unfamiliar, wide, or front-loaded. Preserve complexity that encodes real domain distinctions, durability, failure recovery, or an evidenced investment that simplifies downstream work.
- Do not recommend removing a mechanism until its consumers, operational role, failure behavior, and replacement path are understood. Require a concrete cost and a behavior-preserving alternative.

## Context Budget

Inspect the minimum relevant code needed to understand the current path, contract, local patterns, and risk. Continue reading only when a requirement, behavior boundary, local pattern, or validation path is unclear.

## Simplicity Checks

- Can one existing code path change instead of adding a layer?
- Can current contracts and data shapes remain unchanged?
- Is the abstraction serving repeated real use, not imagined future use?
- What required behavior or operational guarantee does the apparent complexity encode?
- Would removing local complexity move more complexity, risk, or manual work downstream?
- Can the edge case be handled locally?
- Will a maintainer understand it from nearby code?
- Does validation cover behavior users or callers rely on?

## Output

For recommendations:

- **Real requirement**
- **Complexity to preserve**
- **Assumptions to drop**
- **Simpler path**
- **Tradeoffs**
- **Validation**

Use only the headings that add decision value. For implementation, make the scoped change and verify it.

## Stop Rules

Stop once the smallest complete path is clear and either implemented or recommended with validation. Ask only when missing information would materially change the solution.
