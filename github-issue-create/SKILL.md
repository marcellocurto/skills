---
name: github-issue-create
description: Draft and create GitHub issues with `gh`. Use for bugs, tasks, features, PRDs, specs, epics, sub-issues, blockers, and tracer-bullet vertical issue breakdowns. Draft first. After approval, create issues and approved native GitHub relationships in the same turn.
---

# GitHub Issue Create

Turn user, repo, or source-issue context into actionable GitHub issue drafts, then create approved issues and approved native GitHub relationships with `gh`.

`AFK` = implementable end-to-end without human input. `HITL` = blocked on a real human decision such as design, product, or architecture.

For multi-step work, start with a short user-visible update that says what repository or source context you are checking first.

## Goal

Produce issue drafts a maintainer can act on, get explicit approval, then publish exactly the approved issue set.

## Success Criteria

- Drafts use facts from the user, repo, or fetched source issue.
- Each issue has a clear title, observable acceptance criteria, useful metadata, and proportional scope.
- Multi-issue implementation plans are tracer-bullet vertical slices unless an architecture exception is justified.
- Likely duplicates are surfaced before creation.
- No issue, label, or native relationship is created before explicit approval.
- After creation, issue URLs and native relationship status are reported.

## Hard Constraints

- Create only after explicit approval.
- Never duplicate or modify parent/source issues unless asked.
- Do not invent requirements, metadata, labels, relationships, priority, or acceptance criteria.
- Prefer existing labels; draft new labels only with approval.
- Keep titles under 80 characters when practical.
- Bugs need repro, expected/actual behavior, environment, and impact when known.
- Body links do not satisfy approved parent/sub-issue or blocked-by relationships. Create native GitHub relationships.

## Context And Tool Budget

Preflight `gh`, auth, and repo before drafting or publishing. If `gh` is missing, auth fails, or the repo is unclear, stop and report the smallest fix or ask for `owner/name`.

Gather only the context needed to draft correctly: repo, issue type, title/summary, completion criteria, bug repro details, explicit relationships, source issue text/comments, and relevant code/docs/ADRs for implementation issue sets.

Use duplicate search with 2-4 distinctive nouns from the title. Retry broader terms only when empty or ambiguous. Search again only when a required fact, owner, date, source issue, code path, relationship, label, or acceptance criterion is missing.

Read command details from [references/gh-commands.md](references/gh-commands.md) when you need exact `gh` commands, REST endpoints, or relationship verification.

## Tracer-Bullet Issue Architecture

Use this for any plan, spec, PRD, epic, or multi-issue request. Design the breakdown before drafting final issue bodies.

Each implementation issue should deliver one narrow user-visible or operational behavior end-to-end. Include every needed layer for that behavior, such as data, API, worker, UI, docs, tests, and analytics, so the issue is demoable or verifiable after merge.

Avoid layer-only issues such as `create schema`, `add endpoint`, `build UI`, `write tests`, or `wire service`. Fold that work into the first vertical slice that needs it.

Horizontal/enabler issues are exceptions. Use them only for discovery, required decisions, broad migrations, mechanical refactors, or work that is independently valuable. Mark each one:

`Architecture exception: <why this is not a vertical slice>`

Every implementation issue must include one of:

- `Tracer-bullet: yes - <demoable behavior>`
- `Architecture exception: <reason>`

## Native Relationship Contract

Approval of `Parent`, `Sub-issues`, `Blocked by`, or `Blocking` includes approval to create the native GitHub relationship. Do not ask again after issue creation.

- Parent/sub-issue: create or identify child, resolve child REST `id`, then attach it to the parent.
- Blocked-by/blocking: create or identify both issues, resolve the blocking issue REST `id`, then attach the dependency.
- Existing parent issues count when approved as parents.
- Source/context issues do not count as parents unless the user says so.
- Body relationship sections are audit trail only.
- Multi-issue creation is complete only after relationship mutations are attempted and verified, or exact failures are reported.

## Draft

Read the relevant template before drafting: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, or `templates/vertical-slice.md`. Use repo templates when requested or clearly required.

For one issue, follow the template. Show repo, title, body, assignee, labels/new labels, duplicate candidates, milestone/project metadata, and relationships.

For a plan/spec, read `examples/tracer-bullet-breakdown.md`, then draft a numbered tracer-bullet breakdown before final bodies. Each item must show title, kind, `AFK`/`HITL`, parent/source, blockers, end-to-end behavior, demo/verification path, user stories when present, acceptance summary, and architecture check.

Relationship plan: list native relationships to create after approval, such as `Parent: #12 -> #14 via sub_issues` or `Blocked by: #18 blocked by #17 via dependencies/blocked_by`. For new issues, use titles and say IDs will be resolved after creation.

Approval format: repo/title header, issue body under a Body: label, metadata block, relationship plan, then Reply "create" to proceed, or tell me what to change. Do not wrap the draft, body, metadata, relationship plan, or approval prompt in code fences. For multi-issue drafts, include the issue architecture check before the relationship plan.

Use this shape for each draft:

Repo: owner/name
Title: <issue title>

Body:
<exact issue body>

Metadata:
- Assignee: <none or username>
- Labels: <none or labels>
- New labels: <none or labels requiring approval>
- Milestone/project: <none or value>
- Relationships: <none or planned native relationships>

Relationship plan:
- <none or native relationships to create after approval>

Reply "create" to proceed, or tell me what to change.

## Publish

After approval, create only the approved labels, issues, metadata, and relationships. Publish blockers before dependents when issue order matters. Use real issue URLs in body relationship sections when creating issue sets.

On label failure, report the reason and ask whether to drop or retry. On partial multi-issue failure, list created URLs, uncreated issues, and pending relationships; do not retry destructively.

Use [references/gh-commands.md](references/gh-commands.md) for exact commands and verification endpoints.

## Output

Return one line per issue:

`#N - title - URL - labels`

For multi-issue runs, add `Relationships created:` and `Relationships failed/skipped:`. Do not omit relationship status.

## Stop Rules

Stop after showing drafts and wait for approval. After approval, stop only when all approved issues have been created or exact failures are reported, and every approved native relationship has been attempted and verified or reported failed.

## References

- Commands: `references/gh-commands.md`
- Templates: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, `templates/vertical-slice.md`
- Examples: `examples/settings-crash-bug.md`, `examples/multiple-related-issues.md`, `examples/tracer-bullet-breakdown.md`
