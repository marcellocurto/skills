---
name: implement
description: Implement and verify clearly scoped software work from an existing spec or tickets.
---

# Implement

## Objective

Implement every in-scope requirement from the supplied spec or tickets. Continue until the work is complete and verified, or until a genuine blocker requires user input.

## Agree on the work

Before editing, identify:

- **Requirements**: the spec, tickets, repository instructions, user decisions, and input versions that define the work
- **Result**: what must be true when the work is complete
- **What may change**: the code, data, configuration, UI, and artifacts included in the work
- **What must stay unchanged**: existing behavior, contracts, data, and adjacent systems
- **External writes**: writes outside the local working tree and whether the user authorized them
- **How to verify it**: the user or caller workflow and the observations that would prove the result

For clear requests, use this as an internal check. Explain the uncertainty and ask before editing only when the answer would change the solution, require additional authorization, or affect an important risk.

## Constraints

- Treat the spec, tickets, repository instructions, and existing code contracts as the source of truth.
- Treat examples, suggestions, rejected approaches, and future ideas as context rather than requirements unless the source explicitly adopts them.
- Inspect the relevant code before editing. Preserve behavior, data semantics, accessibility, contracts, and sound local conventions unless the requirements explicitly change them.
- Produce the simplest production-quality design for the completed requirement. Place behavior with its natural owner and restructure the affected path when needed to preserve cohesion. Scope limits behavior and product impact, not the number of files, modules, symbols, or lines changed.
- Structural work needed to give the new behavior a clear home is part of the implementation, not unrelated cleanup. A focused module may have one caller when it hides meaningful decisions, state, workflow, policy, or composition behind a smaller interface. Do not add speculative genericity, configurability, extension points, pass-through wrappers, or unrelated refactors.
- Do not infer authorization to change schemas, migrations, export formats, public APIs, external records, business claims, or unrelated shared infrastructure. When the implementation genuinely requires an unapproved expansion, report the dependency and smallest follow-up instead of silently expanding scope.
- When replacing an interface, find everything that uses it, including tests. If you can update all callers together, update them and remove the old interface in the same change. Update tests to use the replacement while still checking the same behavior; do not keep an old production API just to leave tests unchanged. If external callers, mixed versions, or separate deployments require a gradual rollout, keep the old interface until those callers can move. State when each temporary adapter can be removed, and verify who uses an interface before calling it internal.
- If the user corrects an assumption or changes the task, stop work based on the old instruction. Recheck planned and completed changes that depended on it before continuing. Preserve unrelated and user-authored changes.
- Resolve minor uncertainty with evidence from the repository and reasonable assumptions. Ask only when missing information would materially change the result or when the requested approach would create a significant risk.
- Leave changes uncommitted unless the user explicitly requests a commit.

## Execution

1. Confirm the agreed requirements, what may change, what must stay unchanged, and the repository's verification commands.
2. Identify the natural owner of each new responsibility. Inspect the containing function or module far enough to determine whether adding the behavior would give it another independent reason to change. Prefer an existing suitable owner; otherwise create a focused module when it materially reduces what the caller must understand. Predicted reuse is not required.
3. Use `tdd` when writing a failing test first would help design the behavior or catch a realistic regression. Reuse agreed test interfaces. Do not require TDD when that test would provide little useful feedback.
4. Implement the complete solution. Verify that edits were applied as intended and cover all affected paths, including relevant edge cases.
5. Treat implementation friction as design feedback. A single mismatch may be local; repeated deviations of the same shape—unplanned parameters, recurring special cases, escape-hatch types, or callers needing internal rules—require stopping to determine whether the requirements were incomplete, the design is wrong, or the implementation is overreaching. Compare the current approach with a clean target design, then choose an authorized correction that restores a coherent design. Do not silently rewrite adjacent code, change compatibility, or accumulate workarounds.
6. Use `blast-radius-audit` when requested or when the change could affect stored data, serialized formats, public or cross-service APIs, dependency behavior, startup or cleanup timing, runtime configuration, or compatibility during rollout. Do not invoke it merely because the changed code has callers.
7. During implementation, run a narrow check only when its result is likely to influence the next change. Avoid repeatedly running broad lint, typecheck, build, or test commands while the implementation is still evolving.

## Verification

Match verification to the acceptance criteria, affected contracts, and change risk. Complete user-requested and repository-required checks. A straightforward local change may need focused validation and a direct review; use dedicated audits and independent review when they add meaningful confidence.

- **Code checks:** Run the repository's applicable formatting, lint, type, build, and test checks. Run the full test suite when required or when plausible regressions cross enough of the system that focused checks cannot adequately cover them. Do not add a full-suite run solely because implementation is complete.
- **Conformance:** Check every material requirement and protected constraint against implementation evidence. Use `spec-conformance-audit` when explicitly requested or when interacting requirements, conflicting evidence, or possible scope spillover warrant a separate audit. For a straightforward change, check conformance directly without a separate report.
- **Acceptance path:** Exercise the narrowest complete workflow the user or consuming system relies on when acceptance depends on observable behavior or an artifact. Use `user-journey-verifier` when explicitly requested or when a journey spans multiple layers or needs dedicated interaction or artifact inspection; otherwise verify the path directly. A passing lower-level test or direct script does not prove a browser flow, generated document, import, export, or external integration works.
- **Review:** Inspect the completed diff for correctness, regressions, and unnecessary complexity. Use `code-review` when explicitly requested, when repository rules require independent review, or when the change's shared contracts, lifecycle behavior, substantial restructuring, or unresolved concerns warrant it. A direct review is sufficient for a straightforward local change unless independent review is required.

As part of that review, read the callers of new or changed modules and adapters. Check what each module handles that callers would otherwise need to handle themselves. Keep it when it owns useful behavior or protects a required contract, such as cleanup or support for older callers. If it only forwards a call and adds another file to navigate, put that call in the appropriate existing module. File size and caller count alone do not decide this.

Choose the order that resolves the remaining evidence gaps. Conformance does not need to pass before an acceptance-path check runs: a journey result may establish conformance, and a conformance finding may identify the journey that still needs checking. Share relevant requirements, implementation versions, and existing validation results across checks. Reuse evidence only while the implementation and conditions it covers remain applicable.

When fixing how code is organized, check whether the same problem occurs elsewhere in the affected code. Fix confirmed cases within the authorized scope before declaring the problem resolved. Report any known cases outside that scope separately.

Validate audit and review findings, make confirmed in-scope corrections as part of the authorized implementation, and rerun failed or affected checks. Distinguish and report unrelated pre-existing failures. Once applicable checks pass, broaden or repeat verification only for new changes, failures, or unresolved concerns. If required evidence cannot be obtained, report the precise gap rather than treating an unverified claim as satisfied.

## Completion Contract

Finish only when:

- Every in-scope acceptance criterion is implemented.
- The implementation matches the agreed scope, with no unresolved unauthorized changes.
- The changed path remains coherent: entry points and composition modules do not own a new independent workflow, policy, state machine, or substantial implementation detail merely to keep the diff small.
- New or changed wrappers do useful work or protect a required contract; they do not just add another call to follow.
- The relevant user-visible or consumer-visible acceptance path has been verified when accessible; otherwise the missing verification is reported.
- The completed diff has been reviewed for correctness, regressions, and unnecessary complexity.
- Applicable validation passes, or any remaining failure is clearly identified with supporting evidence.
- The final response states what changed, what was validated, and any remaining risk or blocker.
