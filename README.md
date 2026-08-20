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

- **[`simple-answer`](skills/simple-answer/SKILL.md)**: Rewrite the previous answer in short, plain language. Inspired by Cursor PStack's [`bro` skill](https://github.com/cursor/plugins/blob/main/pstack/skills/bro/SKILL.md).
- **[`wayfinder`](skills/wayfinder/SKILL.md)**: Break a large, uncertain effort into decision steps and resolve them until the path is clear.
- **[`design-system-ui`](skills/design-system-ui/SKILL.md)**: Build polished production UI that extends a product's existing design system and patterns.
- **[`wild-frontend`](skills/wild-frontend/SKILL.md)**: Create bold, unconventional frontend designs when product conventions are intentionally not the goal.
- **[`grill-with-docs`](skills/grill-with-docs/SKILL.md)**: Stress-test a plan through questions while recording the resulting domain terms and decisions. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md)
- **[`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md)**: Find high-value ways to deepen a codebase's modules, present them visually, and explore the chosen change. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md)
- **[`to-spec`](skills/to-spec/SKILL.md)**: Turn the current conversation into a specification and publish it to the project's issue tracker. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md)
- **[`triage`](skills/triage/SKILL.md)**: Classify and verify issues and external pull requests, then prepare them for the right next step. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md)

**Model-invoked (implicit allowed)**

- **[`bug-fix-planner`](skills/bug-fix-planner/SKILL.md)**: Investigate one bug and produce an implementation-ready fix plan without changing code.
- **[`implementation-planner`](skills/implementation-planner/SKILL.md)**: Turn a defined feature or refactor into a bounded, implementation-ready plan without changing code.
- **[`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md)**: Reproduce, isolate, and fix difficult bugs or performance regressions. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md)
- **[`explain-codebase`](skills/explain-codebase/SKILL.md)**: Trace and explain how an existing code path or subsystem works. Inspired by Cursor PStack's [`how` skill](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md).
- **[`github-issue-audit`](skills/github-issue-audit/SKILL.md)**: Decide whether one GitHub issue is valid, unique, scoped, and ready to proceed. Inspired by [Roark's](https://github.com/marcellocurto/roark-coding-agent) triage mechanics.
- **[`simplify-code-solution`](skills/simplify-code-solution/SKILL.md)**: Reduce a proposed code change to the smallest solution that fully meets the real requirements.
- **[`to-tickets`](skills/to-tickets/SKILL.md)**: Turn approved work into well-scoped GitHub issues after checking for duplicates and dependencies.
- **[`implement`](skills/implement/SKILL.md)**: Implement and verify clearly scoped software work from an existing spec or tickets.
- **[`create-pull-request`](skills/create-pull-request/SKILL.md)**: Open a ready-for-review GitHub pull request for completed local changes, including any needed commit and push.
- **[`address-review-feedback`](skills/address-review-feedback/SKILL.md)**: Validate pull-request feedback against the current code and requirements, then apply only the fixes the user approves.
- **[`spec-conformance-audit`](skills/spec-conformance-audit/SKILL.md)**: Check whether an implementation matches its source specification and agreed decisions.
- **[`audit-code-complexity`](skills/audit-code-complexity/SKILL.md)**: Find needless code complexity and suggest simpler designs that preserve behavior.
- **[`blast-radius-audit`](skills/blast-radius-audit/SKILL.md)**: Find downstream breakage a code change could cause beyond the files it directly touches. Inspired by Cursor PStack's [`blast-radius` skill](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md).
- **[`test-quality-audit`](skills/test-quality-audit/SKILL.md)**: Judge whether tests catch realistic regressions and recommend what to keep, change, or remove.
- **[`product-ui-audit`](skills/product-ui-audit/SKILL.md)**: Review an existing product interface and recommend a product-specific UX direction without changing code.
- **[`user-journey-verifier`](skills/user-journey-verifier/SKILL.md)**: Verify completed software through the exact user workflow and resulting output, without fixing it.
- **[`relentless-review`](skills/relentless-review/SKILL.md)**: Challenge an existing proposal or result to find material risks and a better path.
- **[`shadcn`](skills/shadcn/SKILL.md)**: Build, update, debug, and style shadcn/ui components using the project's registry and conventions. Source: [`shadcn/ui`](https://github.com/shadcn/ui/tree/main/skills/shadcn).
- **[`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md)**: Apply scalable React composition patterns when designing or refactoring component interfaces. Source: [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns).
- **[`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md)**: Apply Vercel's React and Next.js performance guidance when writing or reviewing code. Source: [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices).
- **[`code-review`](skills/code-review/SKILL.md)**: Review a specific code change for correctness, requirements, maintainability, and repository standards. [Forked from Matt Pocock](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md); review lenses adapted from [`roark-coding-agent`](https://github.com/marcellocurto/roark-coding-agent); adversarial mode inspired by Cursor PStack's [`interrogate` skill](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md).
- **[`codebase-design`](skills/codebase-design/SKILL.md)**: Design small, type-safe interfaces that hide complexity and give domain logic a clear home. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md)
- **[`domain-modeling`](skills/domain-modeling/SKILL.md)**: Define and maintain the codebase's shared domain terms and architectural decisions. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)
- **[`grilling`](skills/grilling/SKILL.md)**: Stress-test an idea or decision through a thorough, structured interview. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
- **[`prototype`](skills/prototype/SKILL.md)**: Build a temporary prototype to answer a specific design or behavior question. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md)
- **[`research`](skills/research/SKILL.md)**: Research a question using trusted primary sources and save the findings as Markdown. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md)
- **[`tdd`](skills/tdd/SKILL.md)**: Build features and bug fixes test-first around meaningful behavior. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
- **[`wizard`](skills/wizard/SKILL.md)**: Create an interactive Bash wizard for setup steps that only a human can complete. [Forked from Matt Pocock.](https://github.com/mattpocock/skills/blob/main/skills/engineering/wizard/SKILL.md)

## Skill Details

### [`address-review-feedback`](skills/address-review-feedback/SKILL.md)

This skill treats pull-request feedback as claims to validate rather than instructions. It judges the concern separately from the proposed remedy, distinguishes current PR blockers from follow-ups and suggestions, and identifies feedback that is already addressed, invalid, stale, or uncertain.

Only approved, evidence-backed current-PR fixes are implemented. The skill verifies the resulting changes against the original concern, PR requirements, relevant callers, and authorized scope, while GitHub replies, thread resolution, commits, pushes, and pull-request mutations remain separately authorized actions.

The disposition model is adapted from [Roark's pull-request revision workflow](https://github.com/marcellocurto/roark-coding-agent).

### [`audit-code-complexity`](skills/audit-code-complexity/SKILL.md)

For auditing a diff, feature, module, or codebase that may have accumulated more machinery than the problem requires. A current-state audit judges the requested target regardless of its history; a change-scoped audit reports only complexity introduced or materially worsened by the specified changes. Both inspect actual behavior, usage, and local conventions before judging abstractions, control flow, state, data ownership, APIs, dependencies, defensive code, and local implementation quality.

The skill separates essential domain complexity from accidental implementation complexity. Every finding must name a concrete cost, point to evidence, and offer a smaller behavior-preserving shape; unfamiliarity, line count, and personal style preferences are not findings by themselves.

It inspects tests only when their harness, setup, fixtures, mocks, or coupling create or conceal complexity in the code under review. Use `test-quality-audit` for a standalone review of test value, coverage, assertions, snapshots, or missing cases.

### [`bug-fix-planner`](skills/bug-fix-planner/SKILL.md)

For bugs that need a real fix plan, not a grab bag of debugging ideas. This skill starts with the available evidence: issue text, logs, repro steps, failing tests, screenshots, and source code when the repo is available.

It is deliberately conservative. The plan should separate confirmed facts from likely causes and unknowns, trace the failing path, choose one primary fix, and define the checks that prove the original bug is gone.

### [`implementation-planner`](skills/implementation-planner/SKILL.md)

For defined feature and refactor work that needs an implementation plan grounded in the current repository. The skill traces the relevant code path, establishes requirements and protected behavior, drafts the smallest complete change, and then taste-checks its file and abstraction surface before presenting one final plan.

The output names concrete acceptance criteria, current-code evidence, expected files and symbols, ordered implementation steps, and validation with realistic regression value. It reports a precise blocker instead of silently resolving material ambiguity. The planning mechanics are adapted from [Roark Coding Agent](https://github.com/marcellocurto/roark-coding-agent) without depending on Roark's structured artifacts or workflow runtime.

### [`blast-radius-audit`](skills/blast-radius-audit/SKILL.md)

For finding downstream breakage that direct diff inspection and symbol search can miss. The audit follows relevant data, timing, runtime-selection, dependency, and operational edges, then identifies the smallest set of facts the change's safety depends on.

Those facts are proven as far as safely practical through exact source, failure-path tracing, focused execution, or the real consumer journey. Unresolved claims remain explicitly unverified, while confirmed, credible, and cleared risks are reported separately. The audit does not authorize repository edits or permanent tests.

### [`design-system-ui`](skills/design-system-ui/SKILL.md)

I wrote this so the agent will first look at other design implementations in the codebase and do UI / UX work based on that. This works great when there is already a strong design foundation in the codebase and based on that new components have to be added.

It works poorly when there is no unified design system or to try create such a system.
This is good for mature codebases.

Before finishing, the skill renders the actual route when accessible, checks representative data volume and content length, compares the result with adjacent product screens, and verifies that every new surface, loader, icon, badge, card, and state communicates something necessary. Static content must not acquire artificial loading UI or layout shifts.

### [`explain-codebase`](skills/explain-codebase/SKILL.md)

For code walkthroughs and onboarding questions that need a reliable working mental model rather than an annotated file tour. The skill starts at a real caller, route, event, job, command, or user action and follows each material handoff to the final output, state change, side effect, or external call.

It tracks how data changes, where state lives, which runtime implementation is selected, and where responsibility crosses module seams. Every material connection is grounded in code, wiring, configuration, tests, or another exact source; unresolved handoffs and historical rationale without evidence remain explicit instead of being guessed. Debugging and architectural critique stay in their dedicated skills.

### [`github-issue-audit`](skills/github-issue-audit/SKILL.md)

For deciding whether one GitHub issue can proceed before anyone plans or implements it. The audit judges the issue's central claim, fit with accepted scope, readiness, and dependency state independently, then returns an evidence-backed outcome without changing the repository or issue.

Reported statements stay separate from verified facts and inference. Already-satisfied, duplicate, and superseded work produces a no-action outcome, while factual clarification, authoritative decisions, and genuine rejection remain distinct. Readiness also stays separate from blocking dependencies, so a well-specified issue can remain ready even when external work prevents it from starting.

The decision model is adapted from [Roark Coding Agent](https://github.com/marcellocurto/roark-coding-agent) without depending on Roark's structured artifacts or workflow runtime.

### [`to-tickets`](skills/to-tickets/SKILL.md)

This skill turns existing context into one or more GitHub issues and checks open and closed issues for overlapping work before drafting anything. Plans, specifications, conversations, existing issues, and explicitly selected pull-request feedback can all serve as sources.

Tickets are written as compact arguments for human review and independent implementation: current situation, evidence, impact, desired outcome, verifiable acceptance criteria, and meaningful scope boundaries. The structure stays proportional to the work, while relevant decisions and prior findings are preserved when they prevent repeated exploration. Publication requires approval and uses existing labels plus GitHub's native parent and blocking relationships.

The workflow remains portable without the GitHub plugin. `gh` provides the complete read and publication path, while an available connector may improve contextual reads. Explicitly requested research can become a durable research ticket, but unknowns are not used to postpone implementation work that should already be ready.

This version is inspired by Matt Pocock's [`to-tickets` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md), but adapted to my specific needs and how I like my GitHub issues to be written.

### [`implement`](skills/implement/SKILL.md)

For implementing an already-defined spec or set of tickets. Before editing, it establishes the source of truth, authorized outcome, affected and protected surfaces, external mutations, and acceptance path. If the user corrects a premise, work derived from that premise is re-evaluated before implementation continues.

After implementation and repository checks, it audits conformance against the scope contract, verifies the real user journey when observable behavior or artifacts matter, and finishes with a code review. Changes remain uncommitted unless the user explicitly requests a commit.

This version is based on and inspired by Matt Pocock's [`implement` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md), adapted for the GPT-5.6 family and this repository's workflow conventions.

### [`create-pull-request`](skills/create-pull-request/SKILL.md)

For publishing completed local work as a real, ready-for-review GitHub pull request. The skill verifies the complete change and repository checks, then writes a simple outcome-based title, a plain-language summary, and a detailed reviewer guide grounded in the actual diff.

It uses explicit repository, base, head, title, and body-file arguments; never creates draft pull requests; and reads the result back from GitHub to verify its public state and contents. It does not merge, force-push, or silently add labels, reviewers, issue edits, or unrelated worktree changes.

The workflow adapts the guarded PR-publication mechanics from [Roark Coding Agent](https://github.com/marcellocurto/roark-coding-agent) into a standalone skill without depending on Roark's runtime artifacts.

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
