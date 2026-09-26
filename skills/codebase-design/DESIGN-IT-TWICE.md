# Design It Twice

Compare alternatives when at least two designs could meet the requirements and repository conventions do not settle the choice. Parallel agents are optional.

Use the interface and responsibility checks in [SKILL.md](SKILL.md).

Skip the exploration cost when existing conventions or constraints already determine the answer. For visual questions that must be judged by feel, build a quick mockup for the user to look at instead.

## Process

### 1. Explain the current problem

Before comparing alternatives, follow representative callers through the current code. Read the relevant interfaces, implementation, tests, glossary, and ADRs to establish what must stay unchanged and what can be redesigned. Do not invent a reason for the current structure when no source explains it.

Briefly explain:

- The capabilities and realistic scenarios callers need
- What callers currently have to know, coordinate, or repeat
- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- Which modules own the behavior and dependencies, and any documented reasons
- One representative current call trace to make the friction concrete

Continue into the comparison unless a missing decision prevents it.

### 2. Develop credible alternatives

Choose the smallest useful candidate set, usually two. Each candidate must satisfy the same known requirements and differ on a consequential design choice, such as ownership, caller responsibilities, or dependency handling. Include the existing approach when it remains viable. Add a candidate only when it exposes another material tradeoff or the user requests it; do not generate designs merely for novelty or a quota.

Develop the candidates directly, or use a bounded set of read-only sub-agents when available and independent exploration is likely to improve the comparison. Give each agent a grounded candidate to explore, the same requirements and evidence, relevant file paths, coupling details, and dependency context from [DEEPENING.md](DEEPENING.md). If delegation is unavailable or adds little value, compare locally.

Evaluate actual caller needs and demonstrated variation. Do not ask a candidate to maximize flexibility, support hypothetical use cases, or hit an arbitrary number of entry points.

Use the architectural distinctions in [SKILL.md](SKILL.md) alongside the project's established vocabulary, explaining mappings where needed.

For each candidate, provide only the detail needed to compare it:

1. **Caller usage first:** call sites that cover the required behavior. Sketch these before designing types or methods.
2. **Interface:** types, methods, parameters, invariants, ordering, and error modes derived from that usage.
3. **Modules:** which module owns each responsibility and how callers reach it.
4. **Internal work:** rules and coordination that callers no longer need to handle.
5. **Dependency strategy:** dependencies and adapters, using [DEEPENING.md](DEEPENING.md).
6. **Trade-offs:** what becomes easier for callers or maintainers, what becomes harder, and why.

Check that the proposed call sites work with the interface. Adjust the interface when they do not, unless a real requirement prevents it. Do not make callers coordinate internal steps merely because the interface was designed first.

### 3. Present and compare

Before presenting a candidate, revise or reject it when:

- Its interface exposes nearly as much complexity as its implementation, or callers must coordinate several methods to complete one operation.
- Callers must handle storage formats, framework objects, wire types, or protocol details that their task does not require.
- Modules are split by execution order—such as load, validate, transform, and save—even though those stages protect the same knowledge and invariants.
- A method merely forwards the same operation and arguments without adding policy, adaptation, or a distinct abstraction.
- Callers must understand internal rules to use the interface correctly.

These are reasons to inspect a design, not automatic bans. Keep it when a concrete requirement justifies the cost and explain why.

Compare what callers must know, how many places must change when a rule changes, and how easily the behavior can be tested. Include the work and risk of migrating callers and checking the result.

Recommend the strongest design under the known constraints and explain the decisive tradeoff. Stop when the comparison supports a choice or identifies the specific evidence or user decision still needed. Do not keep generating alternatives after the decision is clear.
