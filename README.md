# Skills

Agent skills for better outcomes working with LLMs.

I use most of them daily and refine them as gaps surface — by judgment, not benchmarks (for now). 🤞

## Install

```bash
bunx skills add marcellocurto/skills
# or: npx skills add marcellocurto/skills
```

## Available Skills

Skills for planning, building, reviewing, and improving software. All run manually; **User-invoked** run only when explicitly selected, **Model-invoked** may also be auto-selected on match.

**User-invoked (explicit only)**

- **[`shadcn`](skills/shadcn/SKILL.md)**: Build, update, debug, and style shadcn/ui components using the project's registry and conventions.
- **[`frontend-design`](skills/frontend-design/SKILL.md)**: Choose the visual direction, typography, layout, and interface copy when building new UI or reshaping an existing one.
- **[`grill-with-docs`](skills/grill-with-docs/SKILL.md)**: Stress-test a plan through questions while recording the resulting domain terms and lasting architectural decisions in the project's docs.
- **[`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md)**: Find high-value ways to deepen a codebase's modules, present them visually, and explore the chosen change with you.
- **[`implement-to-pr`](skills/implement-to-pr/SKILL.md)**: Implement a GitHub issue or the work agreed in the conversation, run the repository's checks, and open a pull request that is ready for review.
- **[`babysit-pr`](skills/babysit-pr/SKILL.md)**: Watch a pull request, settle review comments from people and Codex as they arrive, and stop once every thread is answered and Codex approves the latest commit, or when something needs you.
- **[`triage`](skills/triage/SKILL.md)**: Assess one GitHub issue for implementation readiness, ask only the questions that block it, and update it after approval.
- **[`valid-issue`](skills/valid-issue/SKILL.md)**: Quickly judge whether one GitHub issue is valid, still relevant, aligned with the project, and worth implementing.

**Model-invoked (implicit allowed)**

- **[`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md)**: Reproduce, isolate, and fix difficult bugs or performance regressions with a feedback loop that proves the fix.
- **[`explain-codebase`](skills/explain-codebase/SKILL.md)**: Trace and explain how an existing code path or subsystem works, from its entry point to its final effect.
- **[`github-issue-audit`](skills/github-issue-audit/SKILL.md)**: Decide whether one GitHub issue is valid, unique, scoped, and ready to proceed, without changing it.
- **[`to-tickets`](skills/to-tickets/SKILL.md)**: Turn approved work into well-scoped GitHub issues after checking for duplicates.
- **[`create-pull-request`](skills/create-pull-request/SKILL.md)**: Open a ready-for-review GitHub pull request for finished local changes, committing and pushing when needed.
- **[`pr-comments-audit`](skills/pr-comments-audit/SKILL.md)**: Audit open PR comments, fix and push the justified ones, and reply to and resolve each thread.
- **[`pr-audit`](skills/pr-audit/SKILL.md)**: Audit a whole PR for merge readiness across correctness, maintainability and complexity, and test quality, then post one actionable comment.
- **[`audit-code-complexity`](skills/audit-code-complexity/SKILL.md)**: Find needless complexity in code and get simpler designs that keep its behavior.
- **[`blast-radius-audit`](skills/blast-radius-audit/SKILL.md)**: Find what a code change could break beyond the files it touches, across callers, data, timing, and runtime wiring.
- **[`test-quality-audit`](skills/test-quality-audit/SKILL.md)**: Judge whether tests catch realistic regressions, and recommend what to keep, change, or remove.
- **[`relentless-review`](skills/relentless-review/SKILL.md)**: Challenge an existing proposal or result to find its material risks and a better path.
- **[`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md)**: Apply Vercel's React composition patterns when designing or refactoring component interfaces.
- **[`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md)**: Apply Vercel's React and Next.js performance guidance while writing or reviewing application code.
- **[`code-review`](skills/code-review/SKILL.md)**: Review a specific diff, pull request, or commit range from independent correctness and maintainability perspectives. Whole-codebase and current-state subsystem audits fall outside this skill.
- **[`codebase-design`](skills/codebase-design/SKILL.md)**: Design small, type-safe interfaces that hide complexity from callers and give domain logic a clear home.
- **[`domain-modeling`](skills/domain-modeling/SKILL.md)**: Define and maintain the codebase's shared domain terms and the architectural decisions behind them.
- **[`grilling`](skills/grilling/SKILL.md)**: Stress-test an idea or decision through focused questions about the assumptions and tradeoffs that matter.
- **[`tdd`](skills/tdd/SKILL.md)**: Use before implementing a feature or bug fix that adds or changes behavior users or callers rely on, even when the request does not mention tests. Not for removals, behavior-preserving refactors, design exploration, prototypes, styling, copy, configuration, or data cleanup.
- **[`wizard`](skills/wizard/SKILL.md)**: Create an interactive Bash wizard for setup steps that only a person can complete, such as credentials, dashboards, or cutovers.

## Sources and Attribution

Several skills are forked, adapted, or inspired by other projects:

- [Anthropic's frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design): `frontend-design`, adapted with scoped planning, a rule for existing design systems, and product-specific copy guidance. The original license is retained.
- [Matt Pocock's skills](https://github.com/mattpocock/skills): `grill-with-docs`, `improve-codebase-architecture`, `triage`, `diagnosing-bugs`, `to-tickets`, `code-review`, `codebase-design`, `domain-modeling`, `grilling`, `tdd`, and `wizard`.
- [Cursor PStack](https://github.com/cursor/plugins/tree/main/pstack/skills): `explain-codebase`, `blast-radius-audit`, and the adversarial mode in `code-review`.
- [Roark Coding Agent](https://github.com/marcellocurto/roark-coding-agent): `pr-audit`, `pr-comments-audit`, `github-issue-audit`, `create-pull-request`, the review-context helper shared by `babysit-pr`, `pr-comments-audit`, and `to-tickets`, and the review lenses in `code-review`.
- [shadcn/ui](https://github.com/shadcn/ui/tree/main/skills/shadcn): `shadcn`. CLI behavior is referenced from the [official CLI documentation](https://ui.shadcn.com/docs/cli).
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills): `vercel-composition-patterns` and `vercel-react-best-practices`.

## Development

Bun project. Install and check with:

```bash
bun install
bun run check
```

Installable skills: [`skills/`](skills/). Automation: [`scripts/`](scripts/).
Tooling: TypeScript 7, Oxlint, Oxfmt. `bun run format` formats files; `bun run lint:fix` applies safe lint fixes.

After editing React performance/composition rules or their section/document metadata, run `bun run react-guidance:build` to regenerate compiled references (`bun run check` catches drift via `react-guidance:check`).

Install all published skills globally for Codex and Claude Code, and remove obsolete skills tracked as belonging to this repository:

```bash
bun run skills:install
```

The installer uses one published Git revision for installation and cleanup, preserves skills from other sources, and removes obsolete entries only after verifying the new installation. It does not install unpublished changes from this checkout. The plain `bunx skills add` command above only adds or updates skills; use `bun run skills:install` from this repository for reconciliation.

List installed skills:

```bash
bunx skills ls -g
```
