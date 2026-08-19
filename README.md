# Skills

This is a collection of agent skills I wrote to improve the outcome of working with LLMs.

Since I mostly use GPT-5.6 Sol, these are optimizied for use with that model.

Most of the skills I use on a daily basis and try to improve them whenever I find they could be better.

This is currently only done by feel not by benchmarking. 🤞

## Install

```bash
bunx skills add marcellocurto/skills
```

```bash
npx skills add marcellocurto/skills
```

## Available Skills

| Skill                                                       | Description                                                                                                                                                   |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`address-review-feedback`](address-review-feedback/SKILL.md) | Explicitly audits pull-request feedback, recommends dispositions, and implements only approved fixes.                                                        |
| [`audit-code-complexity`](audit-code-complexity/SKILL.md)   | Audits code for accidental complexity and behavior-preserving simplifications, including test infrastructure only when it creates or conceals complexity.   |
| [`bug-fix-planner`](bug-fix-planner/SKILL.md)               | Plans a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code.                                    |
| [`design-system-ui`](design-system-ui/SKILL.md)             | Designs and implements polished frontend UI that feels native to the existing product, codebase, component library, and design system.                        |
| [`implement`](implement/SKILL.md)                           | Implements scoped work from a spec or tickets, then verifies and reviews the completed changes without committing automatically.                              |
| [`relentless-review`](relentless-review/SKILL.md)           | Stress-tests work by asking whether it is actually the best path, challenging assumptions, edge cases, and failure modes without forcing unnecessary changes. |
| [`simplify-code-solution`](simplify-code-solution/SKILL.md) | Simplifies code fixes and feature proposals by grounding them in real requirements, existing code, and the smallest complete solution.                        |
| [`test-quality-audit`](test-quality-audit/SKILL.md)         | Audits tests for real bug-finding value and classifies what to keep, fix, cut, or add.                                                                        |
| [`to-tickets`](to-tickets/SKILL.md)                         | Creates user-approved single or multi-issue GitHub ticket sets from existing context, including selected pull-request feedback.                              |
| [`wayfinder`](wayfinder/SKILL.md)                           | Maps large, multi-session work as a route of decisions, keeping it in the current task unless durable coordination is needed.                                 |
| [`wild-frontend`](wild-frontend/SKILL.md)                   | Explicit-only skill for unconstrained, highly creative frontend artifacts outside normal product constraints.                                                 |

## Skill Details

### [`address-review-feedback`](address-review-feedback/SKILL.md)

This explicit-only skill audits pull-request review feedback against the current code before changing anything. It distinguishes actionable findings from feedback that is already addressed, not actionable, or unclear, then presents evidence and recommended dispositions for approval.

Only approved actionable findings are implemented. The skill verifies the resulting changes and re-audits every approved finding, while GitHub replies, thread resolution, commits, pushes, and pull-request mutations remain separately authorized actions.

### [`audit-code-complexity`](audit-code-complexity/SKILL.md)

For auditing a diff, feature, module, or codebase that may have accumulated more machinery than the problem requires. A current-state audit judges the requested target regardless of its history; a change-scoped audit reports only complexity introduced or materially worsened by the specified changes. Both inspect actual behavior, usage, and local conventions before judging abstractions, control flow, state, data ownership, APIs, dependencies, defensive code, and local implementation quality.

The skill separates essential domain complexity from accidental implementation complexity. Every finding must name a concrete cost, point to evidence, and offer a smaller behavior-preserving shape; unfamiliarity, line count, and personal style preferences are not findings by themselves.

It inspects tests only when their harness, setup, fixtures, mocks, or coupling create or conceal complexity in the code under review. Use `test-quality-audit` for a standalone review of test value, coverage, assertions, snapshots, or missing cases.

### [`bug-fix-planner`](bug-fix-planner/SKILL.md)

For bugs that need a real fix plan, not a grab bag of debugging ideas. This skill starts with the available evidence: issue text, logs, repro steps, failing tests, screenshots, and source code when the repo is available.

It is deliberately conservative. The plan should separate confirmed facts from likely causes and unknowns, trace the failing path, choose one primary fix, and define the checks that prove the original bug is gone.

### [`design-system-ui`](design-system-ui/SKILL.md)

I wrote this so the agent will first look at other design implementations in the codebase and do UI / UX work based on that. This works great when there is already a strong design foundation in the codebase and based on that new components have to be added.

It works poorly when there is no unified design system or to try create such a system.
This is good for mature codebases.

### [`to-tickets`](to-tickets/SKILL.md)

This skill turns existing context into one or more GitHub issues and checks open and closed issues for overlapping work before drafting anything. Plans, specifications, conversations, existing issues, and explicitly selected pull-request feedback can all serve as sources.

Tickets are written for human review and independent implementation, preserving relevant decisions, evidence, constraints, and completion signals. Publication requires approval and uses existing labels plus GitHub's native parent and blocking relationships.

The workflow remains portable without the GitHub plugin. `gh` provides the complete read and publication path, while an available connector may improve contextual reads. Explicitly requested research can become a durable research ticket, but unknowns are not used to postpone implementation work that should already be ready.

This version is inspired by Matt Pocock's [`to-tickets` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md), but adapted to my specific needs and how I like my GitHub issues to be written.

### [`implement`](implement/SKILL.md)

For implementing an already-defined spec or set of tickets. This skill keeps feedback loops proportional: use targeted checks when they help during development, then run linting, typechecking, relevant tests, and the full suite after the implementation is complete.

It finishes with a code review and leaves changes uncommitted unless the user explicitly requests a commit.

This version is based on and inspired by Matt Pocock's [`implement` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md), adapted for the GPT-5.6 family and this repository's workflow conventions.

### [`wayfinder`](wayfinder/SKILL.md)

For planning work too large or uncertain to see end-to-end in one task. It names the destination, charts the visible decisions and remaining fog, then resolves one frontier decision at a time until the route is clear.

The map stays in the current task by default. It moves to the issue tracker only when durable coordination is genuinely needed across sessions, owners, or external blockers, where native parent and blocking relationships preserve the route.

This version is inspired by Matt Pocock's [`wayfinder` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md), adapted for the GPT-5.6 family and this repository's workflow conventions.

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
