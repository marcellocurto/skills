# Skills

Collection of Agent Skills for my daily workflows.

All skills in this repository are optimized for use with the GPT-5.6 model family.

## Install

```bash
npx skills add marcellocurto/skills
```

## Available Skills

| Skill                                                             | Description                                                                                                                                                          |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`audit-code-complexity`](audit-code-complexity/SKILL.md)         | Audits code and tests for accidental complexity, poor patterns, overengineering, low-value tests, and behavior-preserving simplifications.                           |
| [`bug-fix-planner`](bug-fix-planner/SKILL.md)                     | Plans a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code.                                           |
| [`design-system-ui`](design-system-ui/SKILL.md)                   | Designs and implements polished frontend UI that feels native to the existing product, codebase, component library, and design system.                               |
| [`implement`](implement/SKILL.md)                                 | Implements scoped work from a spec or tickets, then verifies and reviews the completed changes without committing automatically.                                  |
| [`relentless-review`](relentless-review/SKILL.md)                 | Stress-tests work by asking whether it is actually the best path, challenging assumptions, edge cases, and failure modes without forcing unnecessary changes.        |
| [`simplify-code-solution`](simplify-code-solution/SKILL.md)       | Simplifies code fixes and feature proposals by grounding them in real requirements, existing code, and the smallest complete solution.                               |
| [`test-quality-audit`](test-quality-audit/SKILL.md)               | Audits tests for real bug-finding value and classifies what to keep, fix, cut, or add.                                                                               |
| [`to-tickets`](to-tickets/SKILL.md)                               | Turns plans, specs, issues, or conversations into approved GitHub ticket sets with native relationships and `ready-for-agent` labels.                              |
| [`wild-frontend`](wild-frontend/SKILL.md)                         | Explicit-only skill for unconstrained, highly creative frontend artifacts outside normal product constraints.                                                        |

## Skill Details

### [`audit-code-complexity`](audit-code-complexity/SKILL.md)

For auditing a diff, feature, module, or codebase that may have accumulated more machinery than the problem requires. A current-state audit judges the requested target regardless of its history; a change-scoped audit reports only complexity introduced or materially worsened by the specified changes. Both inspect actual behavior, usage, and local conventions before judging abstractions, control flow, state, data ownership, APIs, dependencies, defensive code, and local implementation quality.

The skill separates essential domain complexity from accidental implementation complexity. Every finding must name a concrete cost, point to evidence, and offer a smaller behavior-preserving shape; unfamiliarity, line count, and personal style preferences are not findings by themselves.

It also judges whether tests earn their maintenance cost. Tests that merely restate configuration, constants, metadata, or implementation details should be fixed or cut unless the exact representation is itself a supported contract; the preferred proof is observable behavior and a realistic regression the test would catch.

### [`bug-fix-planner`](bug-fix-planner/SKILL.md)

For bugs that need a real fix plan, not a grab bag of debugging ideas. This skill starts with the available evidence: issue text, logs, repro steps, failing tests, screenshots, and source code when the repo is available.

It is deliberately conservative. The plan should separate confirmed facts from likely causes and unknowns, trace the failing path, choose one primary fix, and define the checks that prove the original bug is gone.

### [`design-system-ui`](design-system-ui/SKILL.md)

For production UI work that needs taste without drifting away from the product. This skill reads the existing interface first: components, tokens, typography, layout, states, motion, and accessibility patterns.

The aim is not bland consistency. Existing components are the starting material for something sharper: an interface that feels native, intentional, and more refined than the default version the product would otherwise get.

### [`to-tickets`](to-tickets/SKILL.md)

For turning a plan, spec, issue, or conversation into a focused set of GitHub tickets. It preserves meaningful requirements and constraints, keeps cohesive work together, and splits only when scope or safe sequencing genuinely requires it. Publication always requires approval.

Each ticket uses a simple title, opens with a plain-language summary, states implementation goals without task-list checkboxes, and carries forward useful findings from prior research. Actionable tickets receive the existing `ready-for-agent` label. Parent and blocking edges use GitHub's native relationships; dependency state is never represented by a `blocked` label.

### [`implement`](implement/SKILL.md)

For implementing an already-defined spec or set of tickets. This skill keeps feedback loops proportional: use targeted checks when they help during development, then run linting, typechecking, relevant tests, and the full suite after the implementation is complete.

It finishes with a code review and leaves changes uncommitted unless the user explicitly requests a commit.

This version is based on and inspired by Matt Pocock's [`implement` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md), adapted for the GPT-5.6 family and this repository's workflow conventions.

### [`relentless-review`](relentless-review/SKILL.md)

For the moment when "looks reasonable" is not enough. This skill asks whether the work is actually the best path, then pushes on assumptions, edge cases, failure modes, reversibility, and proof.

It is not criticism for its own sake. Sometimes the answer is that the current approach is already the right one. Recommendations should only appear when they materially improve the outcome, and risks should be specific enough to matter.

### [`simplify-code-solution`](simplify-code-solution/SKILL.md)

For code problems where the proposed solution has started to grow extra machinery. This skill grounds the work in the actual requirements and current code before accepting new abstractions, refactors, dependencies, or state.

Simple only wins when it is complete. The target is the smallest solution that still satisfies the requirements, preserves behavior, fits local patterns, and has a clear way to verify it.

### [`test-quality-audit`](test-quality-audit/SKILL.md)

For judging whether tests are earning their keep. It asks the hard question first: what realistic bug or regression would this catch? Then it checks the implementation, public behavior, mocks, fixtures, snapshots, helpers, and nearby tests.

The bias is toward signal over volume. A smaller suite that fails for the right reasons is better than broad coverage that mostly proves mocks, snapshots, fixtures, or private implementation details.

### [`wild-frontend`](wild-frontend/SKILL.md)

For explicitly requested frontend work where memorability matters more than fitting an existing product system. It is meant for strong concepts, custom interaction, unusual composition, and production-grade artifacts with real visual ambition.

The discipline is to commit to one world instead of mixing every idea together. The result should feel distinctive, but still work: responsive, usable, accessible enough for the task, and implemented as real code rather than a mood board.
