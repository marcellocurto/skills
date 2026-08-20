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

## Available Skills

### Engineering

Skills for planning, implementing, reviewing, and improving software work.

All skills can be invoked manually. **User-invoked** skills run only when selected explicitly. **Model-invoked** skills may also be selected automatically when the request matches their description.

**User-invoked (explicit only)**

- **[`wayfinder`](skills/wayfinder/SKILL.md)**: Map work too large or uncertain to plan end-to-end, resolving one decision at a time until the route is clear.
- **[`design-system-ui`](skills/design-system-ui/SKILL.md)**: Design and implement polished product UI that extends an existing codebase or design system.
- **[`wild-frontend`](skills/wild-frontend/SKILL.md)**: Create an unconstrained, highly original frontend when visual ambition matters more than product consistency.
- **[`grill-with-docs`](skills/grill-with-docs/SKILL.md)**: Run a relentless design interview while building the project's glossary and ADRs. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md)
- **[`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md)**: Scan a codebase for deepening opportunities, present them in a visual report, and grill through the selected candidate. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md)
- **[`to-spec`](skills/to-spec/SKILL.md)**: Synthesize the current conversation into a spec and publish it to the project issue tracker. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md)
- **[`triage`](skills/triage/SKILL.md)**: Move issues and external pull requests through the project's triage workflow. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md)

**Model-invoked (implicit allowed)**

- **[`bug-fix-planner`](skills/bug-fix-planner/SKILL.md)**: Investigate one bug or regression and produce an implementation-ready fix plan without changing code.
- **[`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md)**: Diagnose hard bugs and performance regressions through a tight feedback loop. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md)
- **[`simplify-code-solution`](skills/simplify-code-solution/SKILL.md)**: Reduce an overbuilt or speculative coding proposal to the smallest complete solution supported by real requirements.
- **[`to-tickets`](skills/to-tickets/SKILL.md)**: Turn an approved plan, specification, or conversation into focused GitHub issues with duplicate checks and native relationships.
- **[`implement`](skills/implement/SKILL.md)**: Implement and verify an existing specification or set of tickets, finishing with validation and code review.
- **[`address-review-feedback`](skills/address-review-feedback/SKILL.md)**: Audit pull-request feedback against the current code, recommend dispositions, and implement only approved fixes.
- **[`spec-conformance-audit`](skills/spec-conformance-audit/SKILL.md)**: Audit an implementation against its originating requirements, protected constraints, and authorized scope.
- **[`audit-code-complexity`](skills/audit-code-complexity/SKILL.md)**: Audit code for accidental complexity, overengineering, and behavior-preserving simplifications.
- **[`test-quality-audit`](skills/test-quality-audit/SKILL.md)**: Judge tests by realistic bug-finding value and decide what to keep, fix, cut, or add.
- **[`product-ui-audit`](skills/product-ui-audit/SKILL.md)**: Audit an existing interface and recommend one coherent, product-native UX direction without editing code.
- **[`user-journey-verifier`](skills/user-journey-verifier/SKILL.md)**: Verify completed software through the exact user-visible workflow and resulting artifact.
- **[`relentless-review`](skills/relentless-review/SKILL.md)**: Stress-test a proposal, plan, implementation, or design by challenging assumptions and exploring meaningful failure modes.
- **[`shadcn`](skills/shadcn/SKILL.md)**: Add, search, debug, style, and compose shadcn components and registries using current project context. Source: [`shadcn/ui`](https://github.com/shadcn/ui/tree/main/skills/shadcn).
- **[`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md)**: Apply scalable React composition patterns for reusable component APIs and state management. Source: [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns).
- **[`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md)**: Apply Vercel's React and Next.js performance optimization guidelines. Source: [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices).
- **[`code-review`](skills/code-review/SKILL.md)**: Review a diff against repository standards and its originating specification in parallel. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md)
- **[`codebase-design`](skills/codebase-design/SKILL.md)**: Provide the shared vocabulary and principles for designing deep modules. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md)
- **[`domain-modeling`](skills/domain-modeling/SKILL.md)**: Build and sharpen a project's domain model, glossary, and architectural decisions. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)
- **[`grilling`](skills/grilling/SKILL.md)**: Stress-test a plan or design through successive rounds of decision-tree questions. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
- **[`prototype`](skills/prototype/SKILL.md)**: Build a throwaway logic or UI prototype to answer a design question. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md)
- **[`research`](skills/research/SKILL.md)**: Investigate a question using high-trust primary sources and save the findings in the repository. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md)
- **[`tdd`](skills/tdd/SKILL.md)**: Build features and fix bugs through a test-first red-green loop. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
- **[`wizard`](skills/wizard/SKILL.md)**: Generate an interactive Bash wizard for manual setup, credentials, migrations, or cutovers. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/wizard/SKILL.md)

## Skill Details

### [`address-review-feedback`](skills/address-review-feedback/SKILL.md)

This skill audits pull-request review feedback against the current code before changing anything. It distinguishes actionable findings from feedback that is already addressed, not actionable, or unclear, then presents evidence and recommended dispositions for approval.

Only approved actionable findings are implemented. The skill verifies the resulting changes and re-audits every approved finding, while GitHub replies, thread resolution, commits, pushes, and pull-request mutations remain separately authorized actions.

### [`audit-code-complexity`](skills/audit-code-complexity/SKILL.md)

For auditing a diff, feature, module, or codebase that may have accumulated more machinery than the problem requires. A current-state audit judges the requested target regardless of its history; a change-scoped audit reports only complexity introduced or materially worsened by the specified changes. Both inspect actual behavior, usage, and local conventions before judging abstractions, control flow, state, data ownership, APIs, dependencies, defensive code, and local implementation quality.

The skill separates essential domain complexity from accidental implementation complexity. Every finding must name a concrete cost, point to evidence, and offer a smaller behavior-preserving shape; unfamiliarity, line count, and personal style preferences are not findings by themselves.

It inspects tests only when their harness, setup, fixtures, mocks, or coupling create or conceal complexity in the code under review. Use `test-quality-audit` for a standalone review of test value, coverage, assertions, snapshots, or missing cases.

### [`bug-fix-planner`](skills/bug-fix-planner/SKILL.md)

For bugs that need a real fix plan, not a grab bag of debugging ideas. This skill starts with the available evidence: issue text, logs, repro steps, failing tests, screenshots, and source code when the repo is available.

It is deliberately conservative. The plan should separate confirmed facts from likely causes and unknowns, trace the failing path, choose one primary fix, and define the checks that prove the original bug is gone.

### [`design-system-ui`](skills/design-system-ui/SKILL.md)

I wrote this so the agent will first look at other design implementations in the codebase and do UI / UX work based on that. This works great when there is already a strong design foundation in the codebase and based on that new components have to be added.

It works poorly when there is no unified design system or to try create such a system.
This is good for mature codebases.

Before finishing, the skill renders the actual route when accessible, checks representative data volume and content length, compares the result with adjacent product screens, and verifies that every new surface, loader, icon, badge, card, and state communicates something necessary. Static content must not acquire artificial loading UI or layout shifts.

### [`to-tickets`](skills/to-tickets/SKILL.md)

This skill turns existing context into one or more GitHub issues and checks open and closed issues for overlapping work before drafting anything. Plans, specifications, conversations, existing issues, and explicitly selected pull-request feedback can all serve as sources.

Tickets are written for human review and independent implementation, preserving relevant decisions, evidence, constraints, and completion signals. Publication requires approval and uses existing labels plus GitHub's native parent and blocking relationships.

The workflow remains portable without the GitHub plugin. `gh` provides the complete read and publication path, while an available connector may improve contextual reads. Explicitly requested research can become a durable research ticket, but unknowns are not used to postpone implementation work that should already be ready.

This version is inspired by Matt Pocock's [`to-tickets` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md), but adapted to my specific needs and how I like my GitHub issues to be written.

### [`implement`](skills/implement/SKILL.md)

For implementing an already-defined spec or set of tickets. Before editing, it establishes the source of truth, authorized outcome, affected and protected surfaces, external mutations, and acceptance path. If the user corrects a premise, work derived from that premise is re-evaluated before implementation continues.

After implementation and repository checks, it audits conformance against the scope contract, verifies the real user journey when observable behavior or artifacts matter, and finishes with a code review. Changes remain uncommitted unless the user explicitly requests a commit.

This version is based on and inspired by Matt Pocock's [`implement` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md), adapted for the GPT-5.6 family and this repository's workflow conventions.

### [`product-ui-audit`](skills/product-ui-audit/SKILL.md)

For auditing an existing product interface without immediately implementing a redesign. The skill identifies the real user, dominant job, relevant information, realistic scale, and reachable states before judging the screen.

It separates usability defects, missing product behavior, visual weaknesses, and defensible preferences. Recommendations converge on one coherent screen model and favor hierarchy, consolidation, and progressive disclosure over generic cards, badges, loaders, and dashboard chrome.

### [`wayfinder`](skills/wayfinder/SKILL.md)

For planning work too large or uncertain to see end-to-end in one task. It names the destination, charts the visible decisions and remaining fog, then resolves one frontier decision at a time until the route is clear.

The map stays in the current task by default. It moves to the issue tracker only when durable coordination is genuinely needed across sessions, owners, or external blockers, where native parent and blocking relationships preserve the route.

This version is inspired by Matt Pocock's [`wayfinder` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md), adapted for the GPT-5.6 family and this repository's workflow conventions.

### [`relentless-review`](skills/relentless-review/SKILL.md)

For the moment when "looks reasonable" is not enough. This skill asks whether the work is actually the best path, then pushes on assumptions, edge cases, failure modes, reversibility, and proof.

It is not criticism for its own sake. Sometimes the answer is that the current approach is already the right one. Recommendations should only appear when they materially improve the outcome, and risks should be specific enough to matter.

### [`simplify-code-solution`](skills/simplify-code-solution/SKILL.md)

For code problems where the proposed solution has started to grow extra machinery. This skill grounds the work in the actual requirements and current code before accepting new abstractions, refactors, dependencies, or state.

Simple only wins when it is complete. The target is the smallest solution that still satisfies the requirements, preserves behavior, fits local patterns, and has a clear way to verify it. The skill compares total lifecycle complexity rather than initial code size, preserving justified infrastructure, explicit state, domain distinctions, durability, and recovery behavior.

### [`spec-conformance-audit`](skills/spec-conformance-audit/SKILL.md)

For checking whether completed work matches the contract that authorized it. The skill establishes requirements, protected behavior, exclusions, and unresolved decisions from the latest authoritative sources, then traces each one to implementation evidence.

It reports missing, partial, contradicted, and unverified requirements separately from unauthorized expansion. Code quality and personal preference stay out of the audit unless the contract explicitly governs them.

### [`test-quality-audit`](skills/test-quality-audit/SKILL.md)

For judging whether tests are earning their keep. It asks the hard question first: what realistic bug or regression would this catch? Then it checks the implementation, public behavior, mocks, fixtures, snapshots, helpers, and nearby tests.

The bias is toward signal over volume. A smaller suite that fails for the right reasons is better than broad coverage that mostly proves mocks, snapshots, fixtures, or private implementation details.

### [`user-journey-verifier`](skills/user-journey-verifier/SKILL.md)

For proving an outcome through the same path the user actually takes. The skill defines the actor, entry point, actions, expected result, environment, and material states, then verifies the complete journey and final screen, record, download, or artifact.

Substitute paths do not count as proof: a direct export function cannot verify a browser download button, and a passing build cannot verify a rendered PDF. Every acceptance check is reported as passed, failed, or explicitly unverified.

### [`wild-frontend`](skills/wild-frontend/SKILL.md)

For explicitly requested frontend work where memorability matters more than fitting an existing product system. It is meant for strong concepts, custom interaction, unusual composition, and production-grade artifacts with real visual ambition.

The discipline is to commit to one world instead of mixing every idea together. The result should feel distinctive, but still work: responsive, usable, accessible enough for the task, and implemented as real code rather than a mood board.
