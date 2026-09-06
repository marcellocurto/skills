---
name: codebase-design
description: Design small, type-safe interfaces that hide complexity and give domain logic a clear home.
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Apply these principles when designing or restructuring code. The aim is leverage for callers, locality for maintainers, and testability for everyone.

## Glossary

Use these terms to clarify architectural roles while preserving established product and repository vocabulary. Names such as "component," "service," "API," and "boundary" are appropriate when they communicate the project's meaning. Explain the mapping when it matters; do not rename code or domain concepts merely to match this glossary.

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice.

**Interface**: everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics.

**Implementation**: what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**: leverage at the interface. The amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it.

**Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage**: what callers get from depth. More capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality**: what maintainers get from depth. Change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Design from caller usage inward.** Sketch representative call sites before types or methods, then derive the interface from what those callers need. Internal stages, representations, and coordination stay in the implementation unless callers genuinely need to control them.
- **Design the target separately from the migration.** When a new requirement causes repeated structural workarounds, sketch the clean end state without preserving accidental current shape. Then choose the smallest authorized path toward it while keeping required compatibility. This comparison does not authorize a rewrite.
- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **Test the contract at its owning interface.** Protect caller behavior through the module's interface. An internal module may also have its own interface and tests for distinct behavior or invariants. Keep those seams internal; do not make application callers learn implementation details merely to support tests.
- **Justify seams by what they hide or vary.** Multiple adapters are evidence of real variation, not a prerequisite or proof of a useful interface. A single-adapter seam can earn its place by isolating a protocol, side effects, or independently changing policy. Require a concrete reduction in caller knowledge or testing cost; do not invent another adapter or speculative extension point to justify the seam.

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow: interface here includes every fact a caller must know.
- **Ambiguous use of "boundary"**: clarify whether a domain, deployment, or substitution boundary is meant when the distinction affects the design.

## Going deeper

- **Deepening a cluster given its dependencies**, see [DEEPENING.md](DEEPENING.md): dependency categories, seam discipline, and preserving useful test coverage.
- **Designing correctness-critical types**, see [TYPE-DESIGN.md](TYPE-DESIGN.md) when signatures, variants, external data, or escape hatches carry load-bearing invariants.
- **Finding a structural home for domain logic**, see [DOMAIN-STRUCTURE.md](DOMAIN-STRUCTURE.md) when stateful code repeats branches, lifecycle rules, shape assumptions, or access work.
- **Exploring alternative interfaces or architectures**, see [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) when several credible shapes remain after applying repository conventions and known constraints.
