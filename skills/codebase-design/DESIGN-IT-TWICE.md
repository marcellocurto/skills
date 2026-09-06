# Design It Twice

Use a bounded comparison when an architectural choice has at least two credible shapes and repository precedent does not settle it. Parallel agents are optional; the goal is to resolve the design tradeoff.

Uses the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**, **leverage**.

Skip the exploration cost when existing conventions or constraints already determine the answer. Send visual questions that must be judged by feel to the UI branch of `prototype`.

## Process

### 1. Ground and frame the problem space

Before comparing alternatives, trace representative callers through the current system. Read the relevant interface, implementation, tests, domain glossary, and ADRs closely enough to distinguish real constraints from accidental shape. Do not infer the rationale for an ownership or layering decision from the code alone; label it as unknown when no source establishes it.

Then write a user-facing explanation of the problem space for the chosen candidate:

- The capabilities and realistic scenarios callers need
- What callers currently have to know, coordinate, or repeat
- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- The current ownership and seam placement, including any established rationale
- One representative current call trace to make the friction concrete

Share the framing briefly, then continue into the comparison without waiting unless a missing decision prevents it.

### 2. Develop credible alternatives

Choose the smallest useful candidate set, usually two. Each candidate must satisfy the same known requirements and differ on a consequential design choice, such as ownership, caller responsibilities, or dependency handling. Include the existing approach when it remains viable. Add a candidate only when it exposes another material tradeoff or the user requests it; do not generate designs merely for novelty or a quota.

Develop the candidates directly, or use a bounded set of read-only sub-agents when available and independent exploration is likely to improve the comparison. Give each agent a grounded candidate to explore, the same requirements and evidence, relevant file paths, coupling details, and dependency context from [DEEPENING.md](DEEPENING.md). If delegation is unavailable or adds little value, compare locally.

Evaluate actual caller needs and demonstrated variation. Do not ask a candidate to maximize flexibility, support hypothetical use cases, or hit an arbitrary number of entry points.

Use the architectural distinctions in [SKILL.md](SKILL.md) alongside the project's established vocabulary, explaining mappings where needed.

For each candidate, provide only the detail needed to compare it:

1. **Caller usage first:** representative call sites that cover the material needs. Sketch these before designing types or methods.
2. **Interface:** types, methods, parameters, invariants, ordering, and error modes derived from that usage.
3. **Module map:** ownership, seam placement, and the flow between modules.
4. **Hidden implementation:** the knowledge, policy, and coordination callers no longer carry.
5. **Dependency strategy:** dependencies and adapters, using [DEEPENING.md](DEEPENING.md).
6. **Trade-offs:** where leverage is high, where it is thin, and what the design deliberately gives up.

The usage and interface must agree. Reconcile the interface to the caller experience unless a real constraint makes that usage impossible; do not make callers inherit an internal structure merely because it was sketched first.

### 3. Present and compare

Before presenting a candidate, revise or reject it when:

- Its interface exposes nearly as much complexity as its implementation, or callers must coordinate several methods to complete one operation.
- A storage shape, framework object, wire type, policy, or protocol decision leaks across the seam without being part of the caller's real domain contract.
- Modules are split by execution order—such as load, validate, transform, and save—even though those stages protect the same knowledge and invariants.
- A method merely forwards the same operation and arguments without adding policy, adaptation, or a distinct abstraction.
- Callers must understand internal rules to use the interface correctly.

These are design evidence, not automatic bans. Keep a shape when a concrete requirement justifies it and make that trade-off explicit.

Compare the candidates by caller effort, **depth** (leverage at the interface), **locality** (where change concentrates), **seam placement**, and material migration or verification costs.

Recommend the strongest design under the known constraints and explain the decisive tradeoff. Stop when the comparison supports a choice or identifies the specific evidence or user decision still needed. Do not keep generating alternatives after the decision is clear.
