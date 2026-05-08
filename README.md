# Skills

Collection of Agent Skills for my daily workflows.

## Install

```bash
npx skills add marcellocurto/skills
```

## Available Skills

| Skill | Description |
| --- | --- |
| [`bug-fix-planner`](bug-fix-planner/SKILL.md) | Plans a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code. |
| [`design-system-ui`](design-system-ui/SKILL.md) | Designs and implements polished frontend UI that feels native to the existing product, codebase, component library, and design system. |
| [`github-issue-create`](github-issue-create/SKILL.md) | Drafts and creates GitHub issues with `gh`, including bugs, tasks, features, PRD/spec breakdowns, sub-issues, blockers, and vertical slices after explicit approval. |
| [`github-issue-quick-create`](github-issue-quick-create/SKILL.md) | Quickly drafts one straightforward GitHub issue with minimal metadata, then creates it with `gh` after explicit approval. |
| [`nextjs-setup`](nextjs-setup/SKILL.md) | Creates or updates a Next.js app with the preferred Bun, strict TypeScript, ESLint, Prettier, Tailwind, shadcn, non-default port, check script, and AGENTS.md baseline. |
| [`relentless-review`](relentless-review/SKILL.md) | Stress-tests work by asking whether it is actually the best path, challenging assumptions, edge cases, and failure modes without forcing unnecessary changes. |
| [`simplify-code-solution`](simplify-code-solution/SKILL.md) | Simplifies code fixes and feature proposals by grounding them in real requirements, existing code, and the smallest complete solution. |
| [`test-quality-audit`](test-quality-audit/SKILL.md) | Audits tests for real bug-finding value and classifies what to keep, fix, cut, or add. |
| [`wild-frontend`](wild-frontend/SKILL.md) | Explicit-only skill for unconstrained, highly creative frontend artifacts outside normal product constraints. |

## Skill Details

### [`bug-fix-planner`](bug-fix-planner/SKILL.md)

For bugs that need a real fix plan, not a grab bag of debugging ideas. This skill starts with the available evidence: issue text, logs, repro steps, failing tests, screenshots, and source code when the repo is available.

It is deliberately conservative. The plan should separate confirmed facts from likely causes and unknowns, trace the failing path, choose one primary fix, and define the checks that prove the original bug is gone.

### [`design-system-ui`](design-system-ui/SKILL.md)

For production UI work that needs taste without drifting away from the product. This skill reads the existing interface first: components, tokens, typography, layout, states, motion, and accessibility patterns.

The aim is not bland consistency. Existing components are the starting material for something sharper: an interface that feels native, intentional, and more refined than the default version the product would otherwise get.

### [`github-issue-create`](github-issue-create/SKILL.md)

For turning scattered context into GitHub issues a maintainer can actually act on. It drafts first, checks the target repo, reads the right issue template, searches for duplicates, and only creates issues after explicit approval.

It handles both single issues and issue sets: bugs, tasks, features, PRD/spec breakdowns, sub-issues, blockers, and vertical slices. The important restraint is scope control: capture what is known, ask for what is missing, and avoid inventing metadata or acceptance criteria.

### [`github-issue-quick-create`](github-issue-quick-create/SKILL.md)

For filing one straightforward issue without the full planning machinery. This skill keeps the useful safety rail from the full workflow: draft first, create only after explicit approval.

It asks only for essentials that would make the issue unusable, skips duplicate search unless requested, honors only explicit labels or assignees, and escalates to `github-issue-create` for multi-issue work, relationships, PRDs, specs, epics, blockers, or tracer-bullet breakdowns.

### [`nextjs-setup`](nextjs-setup/SKILL.md)

For creating a new Next.js app or hardening an existing one with the preferred baseline. It asks for the target path first, resolves it to an app directory, and either runs `bunx create-next-app@latest` or updates the existing project.

The baseline currently covers Bun-only workflow, strict TypeScript, type-aware ESLint, package-level Prettier rules, Tailwind/shadcn defaults, a non-default Next.js port, `bun run check`, reusable `AGENTS.md` guidance, and frontend component ownership conventions.

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
