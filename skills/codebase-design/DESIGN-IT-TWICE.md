# Design It Twice

Use this parallel sub-agent pattern when the user wants alternative interfaces for a deepening candidate or faces a novel architectural decision with multiple viable shapes and no established precedent. Based on "Design It Twice" (Ousterhout): your first idea is unlikely to be the best.

Uses the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**, **leverage**.

Skip this workflow for mechanical implementation, a localized bug or refactor with a clear target, or a decision whose constraints leave only one viable shape. For novel UI interactions that must be judged by feel, use the UI branch of `prototype` instead.

## Process

### 1. Ground and frame the problem space

Before spawning sub-agents, trace representative callers through the current system. Read the relevant interface, implementation, tests, domain glossary, and ADRs closely enough to distinguish real constraints from accidental shape. Do not infer the rationale for an ownership or layering decision from the code alone; label it as unknown when no source establishes it.

Then write a user-facing explanation of the problem space for the chosen candidate:

- The capabilities and realistic scenarios callers need
- What callers currently have to know, coordinate, or repeat
- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- The current ownership and seam placement, including any established rationale
- One representative current call trace to make the friction concrete

Show this to the user, then immediately proceed to Step 2. The user reads and thinks while the sub-agents work in parallel.

### 2. Spawn sub-agents

Spawn 3+ sub-agents in parallel. Each must produce a **radically different** interface for the deepened module.

Prompt each sub-agent with the grounding evidence, relevant file paths, coupling details, dependency category from [DEEPENING.md](DEEPENING.md), and what sits behind the seam. Give each agent a different design constraint:

- Agent 1: "Minimize the interface: aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility: support many use cases and extension."
- Agent 3: "Optimise for the most common caller: make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Include both [SKILL.md](SKILL.md) vocabulary and CONTEXT.md vocabulary in the brief so each sub-agent names things consistently with the architecture language and the project's domain language.

Each sub-agent outputs:

1. **Caller usage first:** README-style usage plus two or three realistic call sites. Write these before designing types or methods.
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

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated: the user wants a strong read, not a menu.
