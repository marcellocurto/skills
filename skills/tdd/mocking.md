# When to Mock

Choose test doubles by the contract being tested, not whether a dependency is internal, external, or owned by the team. Prefer real collaborators when their behavior or integration is part of the claim and they are practical to exercise.

## Useful isolation

A stub, fake, or mock can help when it:

- controls time, randomness, latency, or a failure that would otherwise be difficult to reproduce
- substitutes a dependency outside the current test's contract so the caller's policy can be exercised directly
- records an interaction that is itself promised behavior, such as the payload sent to a service or the absence of a duplicate side effect

An internal collaborator may be substituted at a meaningful seam under the same criteria. Keep the subject's real behavior in the test; do not mock away the policy, transformation, or integration the test claims to verify.

## Match the double to the claim

Model the dependency's relevant contract accurately, including failure and asynchronous behavior when they matter. A convenient mock response that the real dependency cannot produce gives misleading evidence.

Preserve starting conditions that matter to the claim. Do not seed readiness, enable a capability, run a backfill, or supply configuration in setup unless the supported workflow guarantees it or that condition is explicitly the subject of the test. Tests of an initialized state are useful, but do not prove that deployment or first use establishes it. Exercise the real configuration selection when the claim depends on which path runs.

A test of graceful rejection proves error handling, not availability of the required capability. Verify the supported successful workflow separately. A function test can detect a readiness decision without a real database when it executes that decision and faithfully supplies the relevant state; replacing the entire decision with a successful stub cannot.

Use a real test database when verifying persistence, queries, schema constraints, or transaction semantics. A database double may still be useful for a separate test of caller behavior, such as recovery from a reported storage failure, but it does not prove that the real storage path behaves correctly.

Assert calls, counts, or ordering only when they express a promised interaction. If the contract requires one payment request for duplicate submissions, assert that boundary interaction. Asserting that a private formatting helper ran once usually freezes implementation structure.

## Keep the seam with its owner

Prefer existing dependency interfaces and injection points. A focused internal seam is valid when it exposes a meaningful contract to tests while keeping implementation details hidden from application callers. Do not add public methods, wrappers, or generic configuration solely to make a mock easier to set up.

Shape dependency operations around the behavior their callers actually need. Domain-specific operations can hide transport details, while a generic transport interface may be appropriate when transport is the real contract. Mocking convenience alone does not justify replacing one with the other.

## State the evidence limits

A test with a double establishes behavior under that dependency model. It does not establish real wiring, serialization, database semantics, or remote service behavior that the double replaces. Use focused integration or contract coverage when the requirement or demonstrated risk depends on those properties; do not automatically add another broad suite.
