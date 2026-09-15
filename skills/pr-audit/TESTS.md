# Assess Test Quality

Assess tests against implementation, callers, requirements, and prior protection. Stay within the PR and relevant regression risks; existing tests provide evidence without authorizing unrelated cleanup.

## Establish the signal

For each relevant test group, determine:

1. What observable behavior or meaningful contract does it claim to protect?
2. What does it actually exercise and assert?
3. What realistic bug would make it fail, and why would that bug matter?
4. Could production behavior break while the test remains green?
5. Could a harmless internal refactor break it?
6. Is a unit, integration, contract, end-to-end test, or no test appropriate? Choose a boundary that exposes the regression; isolated unit tests cannot establish that production wiring works.
7. Did the reported validation execute this test under the conditions it needs?

Compare changed assertions, fixtures, mocks, snapshots, skips, and configuration with their predecessors. Name realistic failures newly accepted. Lost protection requires an accepted contract change or evidence the old test was wrong. Interface changes do not justify dropping cases; implementation output does not define expected behavior.

## Investigate patterns through behavior

- **Mocks and fixtures:** do they replace claimed behavior, bypass production wiring, or supply setup the supported workflow lacks? Prepared-state tests do not prove users can reach that state.
- **Assertions and calculated expectations:** check for self-comparisons or repetition of production's flawed computation. Calculated expectations are valid when independently grounded in the contract.
- **Interactions and ordering:** call counts and sequences may protect protocols. Flag private-structure assertions when real behavior can fail undetected or refactoring cost exceeds useful protection.
- **Snapshots and constants:** assess output contracts and semantic changes. Fixed values or snapshot syntax are not defects. Distinguish formats and compatibility guarantees from incidental output, prompt prose, fixtures, and non-critical configuration.
- **Overlapping tests and helpers:** compare detected failures before declaring redundancy. Inspect hidden setup, shared state, excessive mocking, and helpers that obscure behavior or force production machinery solely for tests.
- **Obsolete APIs:** when tests alone retain a replaced API, recommend moving meaningful assertions to its replacement if compatibility permits. Preserve useful boundaries even when only tests call them.
- **Failure paths and timing:** inspect relevant retries, concurrency, partial failure, uncontrolled time, and flaky setup. Error-handling tests do not establish successful use.
- **Selection and prerequisites:** inspect commands, filters, opt-ins, skips, expected failures, and required services. Excluded tests cannot support validation claims. Recommend required deterministic coverage in the required command, with visible failure for missing required prerequisites. Keep optional live-service checks distinct.

Patterns are investigation leads, not automatic defects. Require evidence of weakness before recommending changes.

## Resolve material uncertainty

Use failing-before evidence to assess sensitivity to the defect. A final green run cannot prove a required test-first sequence; missing history is a limitation, not proof it was skipped.

When a focused experiment can resolve important uncertainty, run the unchanged test against a known broken version or one narrow defect in a disposable copy. Do not mutate the reviewed checkout, publish the experiment, or add mutation-testing infrastructure. A surviving test disproves only the protection exercised by that experiment.

## Return actionable conclusions

Classify relevant groups internally as **Keep**, **Fix**, **Cut**, or **Add**:

- **Keep:** meaningful protection at reasonable maintenance cost.
- **Fix:** useful intent, but misses claimed failures or couples to incidental details.
- **Cut:** material noise or cost without distinct meaningful protection.
- **Add:** a named important regression escapes coverage and has a practical behavior-level test.

Return only blockers and material limitations for the consolidated comment. Cite the test or missing behavior seam, escaped regression or maintenance cost, and required improvement. Preserve useful protection. No new tests can be the correct outcome; do not demand tests for prose, trivial wiring, or every helper merely to fill this axis.
