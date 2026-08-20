---
name: implementation-planner
description: Plan implementation-ready feature or refactor work by inspecting the existing code, bounding the change, and refining the proposed approach before edits. Use when requirements are sufficiently defined and the user wants a code plan. Not for bugs, open-ended specification work, large uncertain programs, or direct implementation.
---

# Implementation Planner

Plan only. Do not edit files, apply patches, commit, or implement unless the user explicitly changes the request.

## Goal

Produce one repository-grounded plan that another engineer can implement without reconstructing the conversation or rediscovering the relevant code path.

## Establish the Contract

Identify:

- the authoritative requirements and acceptance criteria
- the concrete outcome the implementation must produce
- non-goals and behavior that must remain unchanged
- material assumptions, unresolved decisions, and authorization boundaries

Treat examples, suggestions, rejected approaches, and future ideas as context unless the source explicitly adopts them. Do not weaken requirements to make the implementation easier.

## Gather Enough Evidence

Start from the request, issue or specification, repository instructions, glossary, ADRs, and prior decisions. Search by domain concept, then inspect only the code needed to understand the current path, ownership, stable seams, consumers, relevant tests, and repository validation commands.

Trace at least one representative path from its caller or entry point to the behavior, state change, or output being modified. Distinguish confirmed repository facts from inferences and unknowns. Stop inspecting once the plan's change boundary and validation path are supported by evidence.

## Draft the Smallest Complete Change

Choose one primary implementation path. Prefer existing modules, interfaces, helpers, types, and data shapes when they can satisfy the requirement cleanly.

Every proposed file, abstraction, dependency, schema change, state mechanism, configuration option, or public interface must have a direct requirement or repository-based reason to exist. Preserve essential complexity that represents real domain rules, compatibility, durability, recovery, security, or operational behavior.

Name the expected files and symbols to change and why. Treat that list as the evidence-backed expected surface, not certainty that later implementation may never challenge. Identify protected contracts or consumers when the change could affect them.

Define validation through observable behavior or a durable module seam. Each proposed test must name the realistic regression it would catch. Include exact existing commands when they can be established from the repository; do not invent commands or require tests that merely mirror implementation details.

## Refine Before Presenting

Taste-check the draft and revise it in place:

- Is the implementation surface proportional to the requirement?
- Does every changed file and new concept earn its place?
- Can an existing path replace a new layer, option, or compatibility mechanism?
- Would the proposal scatter one logical change or give one module unrelated reasons to change?
- Did the draft miss a consumer, repository convention, failure path, or protected behavior?
- Does the validation prove the requirement instead of the proposed implementation?
- Can complexity be removed without moving cost or risk elsewhere?

Keep intentional complexity only when the requirement or repository evidence justifies it. Preserve useful problem-specific reasoning, but omit the draft and refinement history from the final answer unless a discarded approach explains an important decision.

## Readiness

Call the plan ready only when its requirements, current-code evidence, proposed behavior, expected change surface, ordered steps, and validation are concrete enough to implement.

A local, reversible assumption may remain when repository evidence supports it; record it. If a missing decision could materially change user-visible behavior, public contracts, data semantics, security, identity, routing, scope, acceptance criteria, or external authority, do not choose silently. Mark the plan not ready and state the exact decision or evidence needed.

## Output

Keep the plan concise and use only headings that add decision value. A ready plan normally includes:

- **Goal and requirements**: source of truth, required outcome, and verifiable acceptance criteria
- **Current code findings**: relevant files, symbols, flow, constraints, and evidence
- **Proposed changes**: one primary behavior and design path
- **Expected change surface**: files or modules, direct reasons, and protected surfaces
- **Implementation steps**: ordered, coherent vertical steps
- **Validation**: meaningful tests, checks, commands, and the regressions they protect against
- **Non-goals, assumptions, risks, and rollback**: only when material
- **Readiness**: ready, or not ready with the precise blocker

Stop when the refined plan is implementation-ready or when the remaining material blocker is stated precisely. Do not continue reading merely to make the plan look exhaustive.
