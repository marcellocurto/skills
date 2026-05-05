---
name: github-issue-create
description: Draft and create GitHub issues with `gh`. Use for bugs, tasks, features, PRDs, specs, epics, sub-issues, blockers, and tracer-bullet vertical issue breakdowns. Draft first. After approval, create issues and approved native GitHub relationships in the same turn.
---

# GitHub Issue Create

Draft issues, get approval, then create them with `gh`.

`AFK` = implementable end-to-end without human input. `HITL` = blocked on a human decision such as design, product, or architecture.

## Rules

- Create only after explicit approval.
- Never duplicate or modify parent/source issues unless asked.
- Use facts from the user, repo, or fetched source issue. Do not invent requirements, metadata, or acceptance criteria.
- Prefer existing labels; draft new labels only with approval.
- Keep titles under 80 characters when practical; keep acceptance criteria observable and proportional.
- Add tests, docs, rollout, analytics, migrations, or follow-up work only when useful.
- Bugs need repro, expected/actual behavior, environment, and impact when known.
- Search duplicates; ask how to proceed on likely matches.
- Multi-issue implementation plans must use tracer-bullet vertical slices. Do not create layer-only issue sets.
- Prefer `AFK`. Use `HITL` only for a real design, product, or architecture decision.
- Body links do not satisfy approved parent/sub-issue or blocked-by relationships. Create native GitHub relationships.

## Tracer-Bullet Issue Architecture

Use this for any plan, spec, PRD, epic, or multi-issue request. Design the breakdown before drafting final issue bodies.

Each implementation issue must:

- Deliver one narrow user-visible or operational behavior end-to-end.
- Include every needed layer for that behavior: data, API, worker, UI, docs, tests, analytics.
- Be demoable or verifiable after merge.
- Prove behavior in acceptance criteria, not implementation chores.
- Be independently ownable, reviewable, and mergeable.

Reject implementation issues that are mainly `create schema`, `add endpoint`, `build UI`, `write tests`, `wire service`, or another horizontal layer. Fold that work into the first slice that needs it.

Horizontal/enabler issues are exceptions. Use them only for discovery, required decisions, broad migrations, mechanical refactors, or work that is independently valuable. Mark each one:

`Architecture exception: <why this is not a vertical slice>`

Self-check every implementation issue before showing it:

`If this merged alone, what behavior could be demonstrated or verified?`

Required check line:

- `Tracer-bullet: yes - <demoable behavior>`
- or `Architecture exception: <reason>`

## Native Relationship Contract

Approval of `Parent`, `Sub-issues`, `Blocked by`, or `Blocking` includes approval to create the native GitHub relationship. Do not ask again after issue creation.

- Parent/sub-issue: identify parent, create child, resolve child REST `id`, then `POST repos/$repo/issues/$parent_number/sub_issues` with `sub_issue_id`.
- Blocked-by/blocking: identify/create both issues, resolve blocking issue REST `id`, then `POST repos/$repo/issues/$blocked_number/dependencies/blocked_by` with `issue_id`.
- Existing parent issues count when approved as parents.
- Source/context issues do not count as parents unless the user says so.
- Body sections are audit trail only.
- Multi-issue creation is complete only after relationship mutations are attempted and verified, or exact failures are reported.

## Workflow

1. Preflight:

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If `gh` is missing or auth fails, stop and report the fix. If repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

2. Resolve context and metadata:

   ```bash
   gh api user --jq .login  # default assignee when none is named
   gh label list --limit 100
   gh issue list --search "<keywords>" --state all --limit 5
   ```

   Gather only missing essentials: repo, issue type, title/summary, completion criteria, bug repro details, and explicit relationships. Use mentioned assignees; otherwise use the current `gh` user.

   Duplicate search: use 2-4 distinctive nouns from the title, retry broader terms if empty, and ask whether to use/link/proceed on likely matches.

   Source issue/path: fetch full body and comments. For implementation issue sets, inspect relevant code, docs, or ADRs so titles use project language and slices match real integration paths.

   If `gh issue view --comments` fails, use REST:

   ```bash
   repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
   gh api "repos/$repo/issues/<number>"
   gh api "repos/$repo/issues/<number>/comments" --paginate
   ```

3. Draft for approval:

   Read the relevant template first: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, or `templates/vertical-slice.md`. Use repo templates when requested or clearly required.

   For one issue, follow the template. Show repo, title, body, assignee, labels/new labels, duplicate candidates, milestone/project metadata, and relationships.

   For a plan/spec, read `examples/tracer-bullet-breakdown.md`, then draft a numbered tracer-bullet breakdown before final bodies. Each item must show: title, kind, `AFK`/`HITL`, parent/source, blockers, end-to-end behavior, demo/verification path, user stories when present, acceptance summary, and architecture check. Iterate on granularity, dependencies, merge/split choices, and `AFK`/`HITL`. Use `templates/vertical-slice.md` for approved implementation slices.

   Relationship plan: list native relationships to create after approval, e.g. `Parent: #12 -> #14 via sub_issues` and `Blocked by: #18 blocked by #17 via dependencies/blocked_by`. For new issues, use titles and say IDs will be resolved after creation.

   Approval format: repo/title header, fenced full body, metadata block, relationship plan, then `Reply "create" to proceed, or tell me what to change.` For multi-issue drafts, include the issue architecture check before the relationship plan.

4. Publish after approval:

   ```bash
   # If needed:
   gh label create "<name>" --color "<hex>" --description "<description>"

   body_file="$(mktemp -t gh-issue-body.XXXXXX.md)"
   cat > "$body_file" <<'EOF'
   <approved issue body>
   EOF
   gh issue create --title "<title>" --body-file "$body_file"
   rm -f "$body_file"
   ```

   Add `--repo`, `--assignee`, repeated `--label`, `--milestone`, and `--project` only when resolved and approved. For issue sets, publish blockers before dependents; use real URLs in `## Parent` and `## Blocked by`.

   On label failure, report the reason and ask whether to drop or retry. On partial multi-issue failure, list created URLs, uncreated issues, and pending relationships; do not retry destructively.

   Relationship step before final response: if the approved draft or plan contains parent/sub-issue, blocked-by, or blocking relationships, create issues first, then read `examples/multiple-related-issues.md` and run the REST `gh api` commands. Verify sub-issues with `GET repos/$repo/issues/$parent_number/sub_issues`; verify blockers with `GET repos/$repo/issues/$blocked_number/dependencies/blocked_by`. Report exact failures.

## Output

Return one line per issue: `#N - title - URL - labels`. For multi-issue runs, add `Relationships created:` and `Relationships failed/skipped:`. Do not omit this relationship status.

## References

- Templates: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, `templates/vertical-slice.md`
- Examples: `examples/settings-crash-bug.md`, `examples/multiple-related-issues.md`, `examples/tracer-bullet-breakdown.md`
