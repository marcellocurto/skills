---
name: simplify-code-solution
description: Simplify a proposed or existing code solution through recommendations or implementation while preserving requirements and clear ownership.
---

# Simplify Code Solution

Find the simplest complete production design for a code problem.

## Choose the working mode

Infer the mode from what the user wants changed and any authorization already given:

- **Recommend:** For an assessment, proposal review, or question such as "Could this be simpler?", explain the simpler path, tradeoffs, and validation needed. A question about simplification does not authorize file edits. A request to revise a proposal applies to that proposal, not the production code it describes.
- **Implement:** When the user asks to simplify or refactor the code, or to apply a recommended change, make the scoped change and verify it. Honor prior authorization without requesting approval again merely because the analysis produced a recommendation.

When no implementation intent is established, stay in recommendation mode. A preferred design or favorable reaction alone does not authorize implementation. Ask only when a missing decision would materially change the solution or its scope.

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
- When replacing an interface, find everything that uses it, including tests. Update tests to use the replacement while still checking the same behavior. Do not keep an old production API just to leave tests unchanged. Keep it when callers or rollout requirements still need it, and state when any temporary adapter can be removed.
- In implementation mode, establish relevant test results before a behavior-preserving refactor and retain the same meaningful cases afterward. Change an expectation only for an authorized contract change or a demonstrated error in the test. Do not simplify fixtures, mocks, or selection in ways that hide a real failure. If the work includes a behavioral fix, observe a practical regression failing before fixing it; explain any unavailable evidence. Preserve a valid failing regression when an unresolved decision or prerequisite blocks completion.

## Context Budget

Inspect the minimum relevant code needed to understand the current path, contract, local patterns, and risk. Continue reading only when a requirement, behavior boundary, local pattern, or validation path is unclear.

## Simplicity Checks

- Can one existing code path absorb the behavior while remaining coherent, or would a focused module reduce the caller's required context?
- Can current contracts and data shapes remain unchanged?
- Is genericity serving demonstrated variation? Separately, does a responsibility extraction hide meaningful existing complexity even if it has one caller?
- Would removing a wrapper make the code easier to follow, or make callers handle rules, cleanup, or compatibility themselves? Read its callers before recommending removal.
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

Use only the headings that add decision value. For implementation, report what changed, why it reduces complexity, the verification performed, and any material limitation.

## Stop Rules

When you find a way to simplify the code, check whether the same problem occurs elsewhere in the requested scope. Include confirmed cases in the recommendation or authorized cleanup before calling the work complete. Report any known cases outside that scope separately.

In recommendation mode, finish when the simpler production-quality path and its validation plan are clear. In implementation mode, continue through the authorized change and verification; do not stop at a proposal. If a genuine blocker prevents completion, state the missing decision or evidence and what remains unfinished.
