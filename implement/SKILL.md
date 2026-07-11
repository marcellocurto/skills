---
name: implement
description: Implement scoped software work from an existing spec or set of tickets. Use when the requirements are defined and the requested outcome is completed, verified code rather than planning or review alone.
---

# Implement

## Objective

Implement every in-scope requirement from the supplied spec or tickets. Continue until the work is complete and verified, or until a genuine blocker requires user input.

## Constraints

- Treat the spec, tickets, repository instructions, and existing code contracts as the source of truth.
- Inspect the relevant code before editing. Preserve established architecture, behavior, data semantics, accessibility, and local conventions unless the requirements explicitly change them.
- Make the smallest coherent change that fully satisfies the requirements. Do not add speculative abstractions, unrelated cleanup, dependencies, or scope.
- Resolve minor uncertainty with evidence from the repository and reasonable assumptions. Ask only when missing information would materially change the result or when the requested approach would create a significant risk.
- Leave changes uncommitted unless the user explicitly requests a commit.

## Execution

1. Identify the acceptance criteria, affected code paths, and applicable repository verification commands.
2. Use the `tdd` skill at pre-agreed seams when test-first work provides useful design or regression feedback. Do not impose TDD where it adds ceremony without meaningful signal.
3. Implement the complete solution. Verify that edits were applied as intended and cover all affected paths, including relevant edge cases.
4. During implementation, run a narrow check only when its result is likely to influence the next change. Avoid repeatedly running broad lint, typecheck, build, or test commands while the implementation is still evolving.
5. After implementation is complete, run the repository's applicable formatting or lint checks, typecheck, relevant tests, and full test suite once. Fix failures introduced by the work, then rerun only failed or affected checks until they pass. Distinguish and report any unrelated pre-existing failures.
6. Use the `code-review` skill on the completed diff. Address actionable findings and rerun affected checks.

## Completion Contract

Finish only when:

- Every in-scope acceptance criterion is implemented.
- The completed diff has been reviewed for correctness, regressions, and unnecessary complexity.
- Applicable validation passes, or any remaining failure is clearly identified with supporting evidence.
- The final response states what changed, what was validated, and any remaining risk or blocker.
