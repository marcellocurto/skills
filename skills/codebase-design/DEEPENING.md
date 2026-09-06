# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**.

## Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable: merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Deepenable if the stand-in exists. The deepened module is tested with the stand-in running in the test suite. The seam is internal; no port at the module's external interface.

### 3. Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### 4. True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam discipline

- **Adapter count is evidence, not a rule.** Production and test adapters may demonstrate useful variation, but a single-adapter seam may still isolate meaningful protocol, side-effect, or policy knowledge. Judge what the seam hides and what its callers gain. Two adapters do not justify a shallow interface, and a second adapter should not be invented to satisfy a count.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.

## Testing strategy: preserve coverage and signal

- Compare the behavior and realistic regressions protected by existing tests with what the new interface tests actually exercise. Passing higher-level tests or coverage percentages alone do not establish that the same cases remain protected.
- Keep lower-level tests that provide distinct signal, such as important edge cases, complex calculations, or dependency contracts. Their location below the new interface is not evidence that they are redundant.
- Replace tests tied only to removed implementation details, and remove duplicates only when retained checks protect the same meaningful behavior with adequate signal. Preserve useful cases when adapting a test to the new structure.
- Add tests through the deepened module's interface where they protect behavior or interactions that lower-level checks cannot establish. Assert observable outcomes and avoid adding another suite that merely repeats existing coverage.
- During an authorized refactor, run the affected tests to verify retained coverage. For design-only work, state which tests should stay, move, or be removed and why; do not modify them.
