---
name: implement
description: Implement scoped software work from an existing spec or set of tickets. Use when the requirements are defined and the requested outcome is completed, verified code rather than planning or review alone.
---

# Implement

## Objective

Implement every in-scope requirement from the supplied spec or tickets. Continue until the work is complete and verified, or until a genuine blocker requires user input.

## Scope Contract

Before editing, establish a compact internal scope contract:

- **Source of truth**: the controlling spec, tickets, repository instructions, explicit user decisions, and authoritative input versions
- **Authorized outcome**: what must be true when the work is complete
- **Affected surfaces**: the code, data, configuration, UI, and artifacts expected to change
- **Protected surfaces**: behavior, contracts, data, and adjacent systems that must remain unchanged
- **External mutations**: any writes outside the local working tree and whether the request authorizes them
- **Acceptance path**: the user-visible or consumer-visible workflow and evidence that prove completion

Keep the contract implicit for unambiguous work. Surface it and ask before editing only when uncertainty would materially change the solution, authority, or risk.

## Constraints

- Treat the spec, tickets, repository instructions, and existing code contracts as the source of truth.
- Treat examples, suggestions, rejected approaches, and future ideas as context rather than requirements unless the source explicitly adopts them.
- Inspect the relevant code before editing. Preserve established architecture, behavior, data semantics, accessibility, and local conventions unless the requirements explicitly change them.
- Make the smallest coherent change that fully satisfies the requirements. Do not add speculative abstractions, unrelated cleanup, dependencies, or scope.
- Do not infer authorization to change schemas, migrations, export formats, public APIs, external records, business claims, or unrelated shared infrastructure. When the implementation genuinely requires an unapproved expansion, report the dependency and smallest follow-up instead of silently expanding scope.
- When replacing an interface, map its consumers before choosing a rollout. If one coordinated change controls every consumer, update them and remove the old path together. If external consumers, mixed versions, independent deployments, or staged rollout require compatibility, use expand–migrate–contract. Give every temporary adapter a concrete removal condition; do not call an interface internal without evidence.
- If the user corrects a premise or changes the task, stop the superseded work. Re-establish the scope contract and re-evaluate every planned or completed change derived from the invalidated premise before continuing. Preserve unrelated and user-authored changes.
- Resolve minor uncertainty with evidence from the repository and reasonable assumptions. Ask only when missing information would materially change the result or when the requested approach would create a significant risk.
- Leave changes uncommitted unless the user explicitly requests a commit.

## Execution

1. Confirm the scope contract, acceptance criteria, affected code paths, and applicable repository verification commands.
2. Use the `tdd` skill at pre-agreed seams when test-first work provides useful design or regression feedback. Do not impose TDD where it adds ceremony without meaningful signal.
3. Implement the complete solution. Verify that edits were applied as intended and cover all affected paths, including relevant edge cases.
4. Treat implementation friction as design feedback. A single mismatch may be local; repeated deviations of the same shape—unplanned parameters, recurring special cases, escape-hatch types, or callers needing internal rules—require stopping to determine whether the requirements were incomplete, the design is wrong, or the implementation is overreaching. Compare the current approach with a clean target design, then choose the smallest authorized correction. Do not silently rewrite adjacent code, change compatibility, or accumulate workarounds.
5. Use `blast-radius-audit` when the user requests it or the completed change genuinely crosses a hidden edge: persisted or serialized data, public or cross-service contracts, dependency semantics, lifecycle timing, runtime selection, or rollout compatibility. Do not invoke it merely because every change has callers.
6. During implementation, run a narrow check only when its result is likely to influence the next change. Avoid repeatedly running broad lint, typecheck, build, or test commands while the implementation is still evolving.
7. After implementation is complete, run the repository's applicable formatting or lint checks, typecheck, relevant tests, and full test suite once. Fix failures introduced by the work, then rerun only failed or affected checks until they pass. Distinguish and report any unrelated pre-existing failures.
8. Use `spec-conformance-audit` on the completed implementation. Address missing, partial, contradicted, or unauthorized work, then rerun affected validation.
9. When acceptance depends on observable behavior or an artifact, use `user-journey-verifier` after conformance passes. Address failures and verify again through the same entry point and workflow the user or consuming system will use. A passing lower-level test or direct script does not prove a browser flow, generated document, import, export, or external integration works.
10. Use the `code-review` skill on the completed diff. Address actionable findings and rerun affected checks.

## Completion Contract

Finish only when:

- Every in-scope acceptance criterion is implemented.
- The completed implementation conforms to the scope contract, with no unresolved unauthorized expansion.
- The relevant user-visible or consumer-visible acceptance path has been verified when accessible; otherwise the missing verification is reported.
- The completed diff has been reviewed for correctness, regressions, and unnecessary complexity.
- Applicable validation passes, or any remaining failure is clearly identified with supporting evidence.
- The final response states what changed, what was validated, and any remaining risk or blocker.
