---
name: user-journey-verifier
description: Verify completed software through the exact user workflow and resulting output, without fixing it.
---

# User Journey Verifier

Verify the outcome through the same path the user relies on.

Verification does not authorize fixes. Do not edit code, install dependencies, change configuration, deploy, or mutate production or external systems unless the user separately requests that action.

## Goal

Produce direct evidence that the requested user-visible behavior works from its real entry point to its final state or artifact.

## Define the Journey

Establish before running checks:

- the actor and starting state
- the exact entry point and actions
- the expected observable outcome
- the environment, data, and artifact version that matter
- any states or scale conditions material to acceptance

Use the user's stated path when one is provided. A substitute path cannot prove the requested path: directly invoking an export function does not verify a browser download button, and inspecting source data does not verify the generated workbook.

If the authoritative environment, reference artifact, or required access is missing, report the gap rather than silently substituting another source.

## Verify End to End

Exercise the narrowest complete journey. Use available browser, document, PDF, spreadsheet, image, log, or shell capabilities only as needed for the actual outcome.

Check the relevant layers:

- **Entry point**: the user can start the journey as expected
- **Behavior**: actions, state transitions, errors, and recovery behave correctly
- **Result**: the final screen, download, record, or artifact contains the promised outcome
- **Presentation**: layout, copy, dimensions, ordering, formatting, and responsive behavior match acceptance when relevant
- **Persistence**: refresh, retry, restart, or later retrieval preserves state when the contract requires it

Use representative data and scale when the defect or requirement depends on them. Do not claim broad coverage from a happy-path fixture that omits the reported condition.

Local or test verification may perform normal reversible actions required by the journey, such as uploading a fixture or creating disposable test state. Keep artifacts outside the working tree when practical, clean up through the application's normal mechanisms when safe, and do not treat test authority as permission for production or external mutation.

## Verdicts

Classify each acceptance check as:

- `pass`: directly observed through the required path
- `fail`: observed behavior contradicts acceptance
- `unverified`: the required path or evidence could not be exercised

Automated tests, typechecks, builds, logs, and code inspection can support a verdict, but they cannot replace missing user-visible evidence when the outcome is visual, interactive, or artifact-based.

## Output

Lead with the journey-level verdict: pass, fail, or unverified.

Report:

| Acceptance check | Evidence | Result |
| --- | --- | --- |

For a failure, include the shortest reliable reproduction and the observed-versus-expected difference. Name a likely implementation area only when evidence supports it; do not turn verification into speculative diagnosis.

For an unverified result, state the exact missing access, environment, data, or tool and the next check that would close the gap.

## Stop Rules

Stop when every material acceptance check has direct evidence or an explicit verification gap. Never report success solely because a different path, unit test, build, or generated artifact succeeded.
