# Combine Related Modules

Use this guide when combining related modules would let callers complete an operation without coordinating its internal steps. Preserve required dependency behavior and useful tests.

## Dependency categories

Check where each dependency runs and how tests can exercise it. Use the relevant approach below when designing the combined module.

### 1. In-process

For pure calculations or in-memory state with no I/O, combine the related behavior and test it directly through the new interface. No dependency adapter is needed.

### 2. Dependencies with local test substitutes

When a suitable local substitute exists, such as PGLite for Postgres or an in-memory filesystem, tests can run the combined module against it. Keep that dependency interface internal when application callers do not need to choose the dependency.

### 3. Services owned by the team

For a service reached through HTTP, gRPC, or a queue, keep business rules in the module and put transport details behind a dependency interface. Production uses the real transport; tests of the module's rules can use an in-memory implementation. Such tests do not establish that the real network integration works.

### 4. Third-party services

For services such as Stripe or Twilio, accept the service through a dependency interface. Tests of the module can provide a mock that represents the service's relevant behavior.

## Keep dependency details with their owner

- Keep a dependency interface when it hides a protocol, side effects, or rules that callers should not have to handle. It may be useful with one adapter; having two adapters does not by itself justify it. Do not invent a second adapter to justify the design.
- Tests may use internal dependency interfaces without exposing them to application callers. Do not add public methods just because tests need control over a dependency.

## Preserve useful tests

- Compare the behavior and realistic regressions protected by existing tests with what the new interface tests actually exercise. Passing higher-level tests or coverage percentages alone do not establish that the same cases remain protected.
- Keep lower-level tests that catch important failures other tests would miss, such as edge cases, complex calculations, or broken dependency contracts. Being below the new interface does not make a test redundant.
- Update tests tied to removed implementation details while preserving the behavior they check. Remove duplicates only when the retained tests would catch the same failures.
- Add tests through the combined module's interface when they check behavior or interactions that lower-level tests cannot verify. Check observable results rather than adding another suite for the same cases.
- During an authorized refactor, run the affected tests to verify retained coverage. For design-only work, state which tests should stay, move, or be removed and why; do not modify them.
