# Domain Structure

Use this guidance when stateful code repeats the same decisions without one clear owner. This file governs code structure; use `domain-modeling` for terminology, glossaries, and ADRs.

## Establish What the Structure Must Protect

Identify:

- rules that must always hold
- valid transitions and who may perform them
- dominant reads, writes, and lookups
- policy duplicated across callers
- required failure, recovery, ordering, and durability behavior

Group code around the rules it owns. Splitting one concept into processing phases often spreads the same decisions across several modules.

## Warning Signs

- Fields must be kept in sync by convention.
- Several files branch on the same state.
- Callers must remember transition order.
- Updates create states the business does not recognize.
- New features extend the same conditional chain.
- Common lookups repeatedly rebuild missing indexes.

## Match the Structure to the Problem

- Mutually exclusive cases with different data → explicit variants.
- Governed lifecycle with meaningful transition rules → state transition model.
- Repeated selection by a stable key → map or registry.
- Mutations that need one authority → reducer or command entry point.
- Expensive recurring access pattern → index, queue, cache, graph, tree, or normalized collection.
- Shared policy and invariants → deep module.

Adopt the structure only if it removes duplicated rules, invalid states, ordering risk, or repeated work. If it merely adds a layer, keep the direct code.

Preserve real domain distinctions and operational guarantees even when a flatter representation uses fewer lines.
