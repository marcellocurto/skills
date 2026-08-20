---
name: spec-conformance-audit
description: Audit an implementation against its originating specification, issue, plan, or explicit decisions. Use to find missing requirements, partial compliance, contradicted constraints, and unauthorized scope expansion. Read-only; not a general code-quality review.
---

# Spec Conformance Audit

Determine whether the implementation matches what was authorized.

Audit only. Do not edit files, apply fixes, commit, publish, or mutate external systems unless the user separately asks for implementation.

## Goal

Trace every material requirement and protected constraint to observable implementation evidence, while identifying work that changed behavior beyond the agreed scope.

## Establish the Contract

Use the smallest authoritative source set that defines the work:

- the user's latest explicit decisions and corrections
- the named specification, issue, plan, or selected review feedback
- repository instructions and established contracts that the work did not authorize changing

Later explicit decisions override earlier proposals. A suggestion is not a requirement merely because it appears in a plan or prior model response. Current implementation behavior is evidence, not automatically the intended contract.

Extract only what affects the verdict:

- required outcomes and acceptance criteria
- behavior, data, interfaces, and user flows that must remain unchanged
- explicit exclusions and protected surfaces
- unresolved decisions that were not authorized for implementation

If sources materially conflict and their precedence cannot be established, report the conflict instead of inventing a merged requirement.

## Inspect the Implementation

Inspect the relevant diff, current code, affected callers and consumers, and verification evidence. Read surrounding code only when needed to understand a contract, behavior boundary, or possible spillover.

For each material requirement, classify it as:

- `satisfied`: implemented with adequate evidence
- `partial`: some required behavior exists, but the contract is incomplete
- `missing`: no implementation evidence
- `contradicted`: implementation does the opposite of the contract
- `unverified`: implementation may exist, but available evidence cannot establish it

Report **unauthorized expansion** separately when the work changes behavior outside the contract, such as unrelated product surfaces, schemas, export formats, business rules, external records, dependencies, or compatibility policy. Extra code is not automatically unauthorized: require a concrete behavioral, operational, or maintenance consequence beyond the approved scope.

## Evidence Standard

- Cite the exact contract source and implementation location for every material finding.
- Separate observed facts from inference.
- Do not credit a requirement based only on naming, comments, or a test that does not exercise the promised behavior.
- Do not fail conformance for style, architecture, complexity, test quantity, or personal preference unless the contract explicitly governs it.
- When acceptance depends on a user-visible path or generated artifact, state that conformance remains unverified until that path is exercised.

## Output

Lead with a direct verdict: conforming, partially conforming, or non-conforming.

Then provide the smallest useful traceability table:

| Requirement or constraint | Source | Implementation evidence | Status |
| --- | --- | --- | --- |

After the table, include only applicable sections:

- **Unauthorized expansion**: changed surfaces that were not approved
- **Evidence gaps**: claims that cannot yet be verified and the exact proof needed
- **Scope-safe next step**: the smallest correction or verification step, without implementing it

If every material requirement is satisfied and no unauthorized expansion exists, say so directly without inventing findings.

## Stop Rules

Stop when every material requirement and protected constraint has a classification, unauthorized expansion has been checked, and the remaining evidence gaps are explicit.
