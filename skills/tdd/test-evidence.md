# Test Evidence

A test proves only what it observes. Choose the observation and any test doubles by the contract being tested.

## Evidence for common contracts

| Contract | Useful evidence | Insufficient substitute |
| --- | --- | --- |
| A created user can be retrieved | Create and retrieve through the supported interface | A database row alone, without exercising retrieval |
| A write persists the required record | Inspect the real test database using the new record's identity | A mock database method was called |
| Failed work rolls back atomically | Observe the relevant database state after rollback | A rollback helper was invoked |
| Duplicate submissions dispatch one payment request | Observe requests at the payment boundary | A private deduplication helper ran a particular number of times |
| An internal policy enforces a domain invariant | Exercise that policy's interface with a case that violates the invariant | Assert its private fields or intermediate helper sequence |
| Existing records keep working after an upgrade | Run the operation on representative existing data and observe the result | Initialize the new state in setup when the upgrade does not guarantee it |
| A deployed capability is available | Exercise its selected configuration and required outcome | Verify only that missing configuration produces a graceful error |

## Databases

Use a real test database when the claim is about persistence, queries, schema constraints, or transactions. When the promise is committed state that another consumer can see, observe it after commit through an independent connection or the consumer's actual path. A database double can still test caller behavior, such as recovery from a reported storage failure, but it does not prove the real storage path works.

## Test doubles

A stub, fake, or mock is useful when it:

- controls time, randomness, latency, or a failure that is hard to reproduce
- replaces a dependency outside the test's claim so the caller's own logic can be exercised directly
- records an interaction that is itself promised behavior, such as the payload sent to a service or the absence of a duplicate side effect

The double must behave like the real dependency where it matters, including failures and asynchronous behavior. A response the real dependency cannot produce gives misleading evidence.

Assert calls, counts, or ordering only when the contract promises that interaction. Asserting that a private helper ran a certain number of times freezes the implementation's structure without proving the result.

Use existing dependency interfaces and injection points. An internal seam is fine when it exposes a meaningful contract to tests without exposing implementation details to application callers.

## What a double cannot prove

A test with a double proves behavior under that model of the dependency. It does not prove real integration, serialization, database semantics, or remote service behavior. When the requirement depends on those, add a focused integration or contract test. Do not add a broad suite by default.
