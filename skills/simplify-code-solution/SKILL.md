---
name: simplify-code-solution
description: Reduce an overbuilt code proposal to the simplest production-quality design that meets the real requirements.
---

# Simplify Code Solution

Find the simplest complete production design for a code problem.

## Goal

Prefer direct, boring changes that meet every real requirement. Simpler is valid only when it preserves behavior, keeps responsibilities coherent, fits sound existing patterns, and can be verified. Fewer files, functions, or modules do not by themselves make a solution simpler.

## Success Criteria

- The actual problem and success criteria are explicit.
- Requirements are separated from assumptions and nice-to-haves.
- Relevant code has been inspected before judging the approach.
- Essential complexity that represents real domain, durability, recovery, or operational requirements is identified and preserved.
- Every proposed generic abstraction, refactor, dependency, or state change is justified by a real requirement or by current complexity it meaningfully hides from callers.
- The recommendation or implementation is the simplest production-quality change that preserves behavior and fits sound local patterns.
- Tradeoffs and validation are stated.

## Constraints

- Reuse existing paths, helpers, types, components, and APIs when they can absorb the behavior without gaining an unrelated responsibility.
- Avoid rewrites for localized bugs, state machines for simple state, generic frameworks for one caller, speculative migrations, unnecessary dependencies, wide API changes for internal convenience, and tests that only mirror implementation.
- Compare total lifecycle complexity, not merely initial implementation size. Do not reject justified infrastructure, durable queues, explicit state, or domain distinctions simply because they add code. Complexity is removable only when requirements, operational guarantees, and failure modes remain covered.
- Do not recommend removing a mechanism until its consumers, operational role, failure behavior, and replacement path are understood. Require a concrete cost and a behavior-preserving alternative.

## Context Budget

Inspect the minimum relevant code needed to understand the current path, contract, local patterns, and risk. Continue reading only when a requirement, behavior boundary, local pattern, or validation path is unclear.

## Simplicity Checks

- Can one existing code path absorb the behavior while remaining coherent, or would a focused module reduce the caller's required context?
- Can current contracts and data shapes remain unchanged?
- Is genericity serving demonstrated variation? Separately, does a responsibility extraction hide meaningful existing complexity even if it has one caller?
- What required behavior or operational guarantee does the apparent complexity encode?
- Would removing local complexity move more complexity, risk, or manual work downstream?
- Can the edge case be handled by its natural owner without making that owner responsible for an independent workflow or policy?
- Will a maintainer understand the changed path without holding unrelated responsibilities in mind?
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

Stop once the simplest production-quality path is clear and either implemented or recommended with validation. Ask only when missing information would materially change the solution.
