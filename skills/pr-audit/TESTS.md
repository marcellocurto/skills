# Assess Test Quality

Audit the tests against the implementation, callers, requirements, and prior protection. Keep this assessment within the PR's contribution and relevant regression risks. Existing tests can establish coverage or reveal a gap without becoming a mandate to clean up unrelated tests.

## Establish the signal

For each relevant test group, determine:

1. What observable behavior or meaningful contract does it claim to protect?
2. What does it actually exercise and assert?
3. What realistic bug would make it fail, and why would that bug matter?
4. Could production behavior break while the test remains green?
5. Could a harmless internal refactor break it?
6. Did the reported validation execute this test under the conditions it needs?

Compare changed assertions, fixtures, mocks, snapshots, skips, and configuration with their previous versions. Name any realistic failure the old test rejected that the new one accepts. Lost protection needs an accepted contract change or evidence that the old test was wrong. Adapting an interface does not justify losing meaningful cases, and current implementation output is not authority for an expected result.

## Investigate patterns through behavior

- **Mocks and fixtures:** check whether they replace the behavior being claimed, bypass production wiring, or repair setup that the supported workflow lacks. Prepared-state tests can be valid without proving that real users can reach that state.
- **Assertions and calculated expectations:** look for tests comparing values with themselves or reproducing the same flawed computation as production. Computed expectations remain useful when grounded independently in the contract.
- **Interactions and ordering:** call counts and sequences can protect real protocols or guarantees. Flag them only when they freeze private structure while observable behavior can still fail, or create concrete refactoring cost without useful protection.
- **Snapshots and constants:** assess the output contract and semantic changes. Neither syntax nor fixed values make a test bad. Distinguish published formats and compatibility guarantees from incidental output, prompt prose, fixtures, and non-critical configuration.
- **Overlapping tests and helpers:** compare the failures they detect before declaring redundancy. Inspect hidden setup, shared state, excessive mocking, and helper layers that obscure the behavior or force production-only-for-tests machinery.
- **Obsolete APIs:** check whether tests are the only reason a replaced API remains. Preserve meaningful assertions through the replacement when compatibility no longer requires the old surface; do not remove a useful boundary merely because only tests call it.
- **Failure paths and timing:** investigate retries, concurrency, partial failure, uncontrolled time, and flaky setup when the PR makes those risks relevant. Error-handling tests do not establish that successful use works.
- **Selection and prerequisites:** inspect actual commands, filters, opt-ins, skips, expected failures, and required services. Excluded tests cannot substantiate a validation claim. Keep optional live-service checks distinguishable from required deterministic checks.

Treat patterns as investigation leads, not automatic defects. Do not require the author to defend every mock, snapshot, or unit test simply because it exists.

## Resolve material uncertainty

Use available failing-before evidence when it demonstrates sensitivity to the relevant defect. A final green run alone cannot prove a required test-first sequence; missing history is a limitation, not evidence of misconduct.

If important protection remains uncertain and a focused experiment can settle it, use a disposable copy to run the unchanged test against a known broken version or one narrowly introduced defect. Never mutate the reviewed checkout or publish the experimental change. Do not add mutation-testing infrastructure. Report only what that experiment establishes; a test surviving one mutation disproves only that particular protection.

## Return actionable conclusions

Classify relevant groups internally as **Keep**, **Fix**, **Cut**, or **Add**:

- **Keep:** protects meaningful behavior at a reasonable maintenance cost.
- **Fix:** has useful intent, but misses the claimed failure or couples to incidental implementation details.
- **Cut:** adds material noise or maintenance cost without distinct meaningful protection.
- **Add:** a named important regression can escape existing coverage and has a practical behavior-level test.

Only send merge-blocking findings and material limitations to the consolidated comment. For each, cite the test or missing behavior seam, identify the realistic escaped failure or concrete maintenance cost, and describe the required improvement. Preserve useful protection in every proposed remedy. A correct absence of new tests can pass; do not demand tests for static prose, trivial wiring, or every helper merely to fill this axis.
