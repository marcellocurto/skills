---
name: github-issue-create
description: Draft and create GitHub issues with `gh`. Use for filing bugs/tasks/features, turning PRDs/specs/plans/epics into issues or tickets, creating sub-issues, setting blockers, or splitting work into vertical slices. Draft first; after approval create the issues and any approved native GitHub parent/sub-issue or blocked-by relationships in the same turn.
---

# GitHub Issue Create

Draft GitHub issues, get approval, then create them with `gh`, including approved native GitHub relationships.

`AFK` = implementable end-to-end without human input. `HITL` = blocked on a human decision such as design, product, or architecture.

## Rules

- Create only after explicit approval; never duplicate or modify parent/source issues unless asked.
- Use facts from the user, repo, or fetched source issue. Do not invent requirements, metadata, or acceptance criteria.
- Prefer existing labels; draft new labels only with approval.
- Keep titles under 80 characters when practical; keep acceptance criteria observable and proportional.
- Add tests, docs, rollout, analytics, migrations, or follow-up work only when useful.
- Bugs need repro, expected/actual behavior, environment, and impact when known.
- Search duplicates; ask how to proceed on likely matches.
- For issue sets, use vertical slices: the smallest end-to-end behavior that can be implemented, verified, and reviewed independently. Avoid layer-only tickets unless the layer work is independently valuable.
- Prefer `AFK`; mark `HITL` only when implementation is blocked by a real human decision, design review, product call, or architecture choice.
- Body links are not enough for approved parent/sub-issue or blocked-by relationships. Create the native GitHub relationships before the final response.

## Native Relationship Contract

If the approved draft includes `Parent`, `Sub-issues`, `Blocked by`, or `Blocking`, that approval includes the GitHub relationship mutations. Do not ask for separate approval after issue creation.

- Parent/sub-issue: create the child issue, resolve the child issue REST `id`, then call `POST repos/$repo/issues/$parent_number/sub_issues` with `sub_issue_id`.
- Blocked-by/blocking: create both issues, resolve the blocking issue REST `id`, then call `POST repos/$repo/issues/$blocked_number/dependencies/blocked_by` with `issue_id` = the blocking issue.
- Existing parent issues count too when the user approved a parent/sub-issue relationship to that issue. Do not mutate a source issue that was only used as context unless the user asked for it to be the parent.
- `## Parent` and `## Blocked by` sections in issue bodies are only an audit trail. They do not satisfy the request by themselves.
- A multi-issue create is not complete until all approved relationship mutations have been attempted and verified, or exact failures are reported.

## Workflow

1. Preflight:

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If `gh` is missing or auth fails, stop and tell the user to install `gh` or run `gh auth login`. If repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

2. Resolve context and metadata:

   ```bash
   gh api user --jq .login  # default assignee when none is named
   gh label list --limit 100
   gh issue list --search "<keywords>" --state all --limit 5
   ```

   Gather only missing essentials: repo, issue type, title/summary, completion criteria, bug repro details, and explicit relationships. Use mentioned assignees; otherwise default to the current `gh` user.

   Duplicate search: use 2-4 distinctive nouns from the title, retry broader terms if empty, and ask whether to use/link/proceed on likely matches.

   Source issue/path: fetch full body and comments. Implementation issue sets: briefly inspect relevant code, docs, or ADRs when available so titles use project language.

   If `gh issue view --comments` fails, use REST:

   ```bash
   repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
   gh api "repos/$repo/issues/<number>"
   gh api "repos/$repo/issues/<number>/comments" --paginate
   ```

3. Draft for approval:

   Read the relevant template first: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, or `templates/vertical-slice.md`. Use repo templates when requested or clearly required.

   For one issue, follow the template. Show repo, title, body, assignee, labels/new labels, duplicate candidates, milestone/project metadata, and relationships.

   For a plan/spec, draft a numbered breakdown before final bodies. Each item must show title, kind (`Tracking` or `Implementation`), type (`AFK`/`HITL` for implementation only), parent/source, blockers, user stories when present, and acceptance summary. Ask about granularity, dependencies, merge/split choices, and `AFK`/`HITL`; iterate until approved. Use `templates/vertical-slice.md` for approved implementation slices.

   Relationship plan: explicitly list native GitHub relationships that will be created after approval, for example `Parent: #12 -> #14 via sub_issues` and `Blocked by: #18 blocked by #17 via dependencies/blocked_by`. For not-yet-created issues, list titles and say IDs will be resolved after creation.

   Approval format: repo/title header, fenced full body, metadata block, relationship plan, then `Reply "create" to proceed, or tell me what to change.`

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

   Relationship step, before final response: if the approved draft or relationship plan contains parent/sub-issue, blocked-by, or blocking relationships, create the issues first, then read `examples/multiple-related-issues.md` and run the REST `gh api` follow-up commands. Verify sub-issues with `GET repos/$repo/issues/$parent_number/sub_issues`; verify blockers with `GET repos/$repo/issues/$blocked_number/dependencies/blocked_by`. If a relationship command fails, report exactly which relationships were not created; keep textual issue links in the bodies.

## Output

Return one line per issue: `#N - title - URL - labels`. For multi-issue runs, add `Relationships created:` and `Relationships failed/skipped:`. Do not omit this relationship status.

## References

- Templates: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, `templates/vertical-slice.md`
- Examples: `examples/settings-crash-bug.md`, `examples/multiple-related-issues.md`
