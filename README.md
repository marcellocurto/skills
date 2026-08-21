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

Skills for planning, building, reviewing, and improving software.

All skills can be invoked manually. **User-invoked** skills run only when selected explicitly. **Model-invoked** skills may also be selected automatically when the request matches their description.

**User-invoked (explicit only)**

- **[`simple-answer`](skills/simple-answer/SKILL.md)**: Use this when an answer is technically correct but harder to understand than it needs to be.
- **[`wayfinder`](skills/wayfinder/SKILL.md)**: Turn a large, foggy project into a shared sequence of decisions without pretending the whole plan is already known.
- **[`design-system-ui`](skills/design-system-ui/SKILL.md)**: Add production UI to a mature product by learning and extending the design patterns already in its codebase.
- **[`wild-frontend`](skills/wild-frontend/SKILL.md)**: Create visually ambitious frontend work that should feel original instead of blending into an existing product system.
- **[`grill-with-docs`](skills/grill-with-docs/SKILL.md)**: Pressure-test a design through conversation while keeping its glossary and architectural decisions up to date.
- **[`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md)**: Surface the architecture changes most likely to improve maintainability, show them visually, and explore the strongest candidate together.
- **[`to-spec`](skills/to-spec/SKILL.md)**: Publish the decisions already made in a conversation as a coherent project specification without reopening the interview.
- **[`triage`](skills/triage/SKILL.md)**: Assess one supplied GitHub issue, resolve only the questions blocking implementation, and update it after approval.

**Model-invoked (implicit allowed)**

- **[`bug-fix-planner`](skills/bug-fix-planner/SKILL.md)**: Use this when a bug needs a credible, code-grounded repair plan before anyone starts editing.
- **[`implementation-planner`](skills/implementation-planner/SKILL.md)**: Turn a settled feature or refactor into a concrete plan that is small enough to implement and verify.
- **[`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md)**: Debug stubborn failures by building a reproducible feedback loop, narrowing the cause, and proving the fix.
- **[`explain-codebase`](skills/explain-codebase/SKILL.md)**: Get a reliable mental model of how a feature actually runs, from its entry point to its final effect.
- **[`github-issue-audit`](skills/github-issue-audit/SKILL.md)**: Find out whether a GitHub issue is true, in scope, ready, duplicated, blocked, or already solved.
- **[`simplify-code-solution`](skills/simplify-code-solution/SKILL.md)**: Challenge an oversized coding proposal and cut it back to the smallest complete solution the requirements justify.
- **[`to-tickets`](skills/to-tickets/SKILL.md)**: Convert approved work into GitHub issues that are focused, self-contained, non-duplicative, and ready for the right owner.
- **[`implement`](skills/implement/SKILL.md)**: Take an existing specification or ticket set through code changes, verification, conformance review, and final quality review.
- **[`create-pull-request`](skills/create-pull-request/SKILL.md)**: Publish finished local work as a real GitHub pull request that is easy for a reviewer to understand and verify.
- **[`address-review-feedback`](skills/address-review-feedback/SKILL.md)**: Check whether review comments are correct before changing code, then implement only the fixes you approve.
- **[`spec-conformance-audit`](skills/spec-conformance-audit/SKILL.md)**: Check completed work against the decisions and requirements that authorized it without turning the audit into general code review.
- **[`audit-code-complexity`](skills/audit-code-complexity/SKILL.md)**: Find code that is harder to understand or change than the problem requires and identify safer, simpler shapes.
- **[`blast-radius-audit`](skills/blast-radius-audit/SKILL.md)**: Trace what a change could break outside the obvious diff, especially across data, timing, persistence, dependencies, and runtime wiring.
- **[`test-quality-audit`](skills/test-quality-audit/SKILL.md)**: Separate tests that catch realistic regressions from tests that mostly add maintenance cost or reassuring coverage numbers.
- **[`product-ui-audit`](skills/product-ui-audit/SKILL.md)**: Evaluate an existing interface in its real product context and converge on one practical UX direction before implementation.
- **[`user-journey-verifier`](skills/user-journey-verifier/SKILL.md)**: Prove that completed software works through the exact path and artifact a real user experiences.
- **[`relentless-review`](skills/relentless-review/SKILL.md)**: Ask whether a proposal or result is genuinely the best path by pushing on its risks, assumptions, and alternatives.
- **[`shadcn`](skills/shadcn/SKILL.md)**: Use the shadcn CLI and registry correctly when adding, composing, styling, or repairing components in a shadcn project.
- **[`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md)**: Apply Vercel's React composition techniques when component APIs become rigid, tangled, or overloaded with boolean props.
- **[`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md)**: Apply Vercel's React and Next.js performance guidance while writing or reviewing application code.
- **[`code-review`](skills/code-review/SKILL.md)**: Review a fixed change from independent correctness and maintainability perspectives, with focused adversarial review when the risk warrants it.
- **[`codebase-design`](skills/codebase-design/SKILL.md)**: Shape code around deep modules, small type-safe interfaces, clear seams, and a natural home for domain logic.
- **[`domain-modeling`](skills/domain-modeling/SKILL.md)**: Keep the codebase's language, glossary, and lasting architectural decisions aligned with the domain people actually discuss.
- **[`grilling`](skills/grilling/SKILL.md)**: Turn a vague plan or decision into shared understanding through structured questions that expose every important branch.
- **[`prototype`](skills/prototype/SKILL.md)**: Build the cheapest useful artifact that can answer a design or behavior question before committing to a full implementation.
- **[`research`](skills/research/SKILL.md)**: Delegate focused reading to a background agent and keep the resulting primary-source findings in the repository.
- **[`tdd`](skills/tdd/SKILL.md)**: Drive a feature or bug fix from meaningful failing behavior through to a verified implementation.
- **[`wizard`](skills/wizard/SKILL.md)**: Package setup steps that require a person—credentials, dashboards, migrations, or cutovers—into a guided interactive Bash flow.

## Sources and Attribution

Several skills are forked, adapted, or inspired by other projects:

- [Matt Pocock's skills](https://github.com/mattpocock/skills): `grill-with-docs`, `improve-codebase-architecture`, `to-spec`, `triage`, `diagnosing-bugs`, `to-tickets`, `implement`, `wayfinder`, `code-review`, `codebase-design`, `domain-modeling`, `grilling`, `prototype`, `research`, `tdd`, and `wizard`.
- [Cursor PStack](https://github.com/cursor/plugins/tree/main/pstack/skills): `simple-answer`, `explain-codebase`, `blast-radius-audit`, and the adversarial mode in `code-review`.
- [Roark Coding Agent](https://github.com/marcellocurto/roark-coding-agent): `address-review-feedback`, `implementation-planner`, `github-issue-audit`, `create-pull-request`, and the review lenses in `code-review`.
- [shadcn/ui](https://github.com/shadcn/ui/tree/main/skills/shadcn): `shadcn`.
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills): `vercel-composition-patterns` and `vercel-react-best-practices`.

## Development

This repository is a Bun project. Install its development dependencies and run all repository checks with:

```bash
bun install
bun run check
```

Installable skills live in [`skills/`](skills/). Repository-level automation lives in [`scripts/`](scripts/).
The tooling uses TypeScript 7, Oxlint, and Oxfmt. Run `bun run format` to format repository files and `bun run lint:fix` to apply safe lint fixes.

Install every published skill globally for Codex and Claude Code with symlinks:

```bash
bun run skills:install
```

List installed skills:

```bash
bunx skills ls -g
```
