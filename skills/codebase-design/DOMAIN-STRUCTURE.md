# Domain Structure

Use this guidance when stateful logic, repeated branches, or duplicated shape assumptions suggest that domain knowledge has no clear structural home. This is about how code represents the domain. Use `domain-modeling` when the domain language, glossary, or ADRs themselves need to change.

## Start From Knowledge and Access

Identify:

- the invariants the system must never violate
- the transitions that are valid and who owns them
- the dominant reads, writes, and lookups
- the policy or representation repeated across callers
- the failure, recovery, ordering, and durability requirements that are real domain complexity

Choose a structure that makes those facts local. Do not organize modules merely by execution order—load, validate, transform, save—when every stage protects the same knowledge.

## Signals That the Shape Is Missing

- Two or more booleans or optional fields must stay synchronized.
- Several files branch on the same state or repeat the same shape assumption.
- Callers must perform lifecycle checks in the correct order.
- Mutations can create intermediate states that the domain considers meaningless.
- Each new feature extends the same conditional chain or duplicates another rule.
- The dominant lookup or update repeatedly reconstructs an index the data model does not provide.

## Choose the Smallest Fitting Structure

- Use explicit variants when cases carry different valid data.
- Use a state machine when transitions, ordering, and invalid moves are load-bearing—not merely because a value has several labels.
- Use a map, registry, or lookup table when branching selects stable behavior by a key.
- Use a reducer or command model when state transitions need one canonical authority.
- Use an index, queue, cache, graph, tree, or normalized collection when the real access pattern calls for it.
- Use a deep module when repeated policy, behavior, and invariants belong to one body of domain knowledge.

The chosen structure should remove branches, duplicated rules, invalid states, lifecycle risk, or repeated work. If it only relocates the same complexity behind another abstraction, keep the direct code.

Preserve genuine domain distinctions and operational guarantees even when a flatter representation would use fewer lines. If the new structure exposes ambiguity in the project's language, resolve that separately through `domain-modeling`.
