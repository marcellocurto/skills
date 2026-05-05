---
name: github-issue-create
description: Draft and create GitHub issues from user context using `gh issue create`. Use when asked to write, create, open, file, log, raise, or track an issue/ticket/bug in GitHub. Draft first and create only after explicit approval.
---

# GitHub Issue Create

Create one or more GitHub issues from the user's context. Draft first; run `gh issue create` only after explicit approval. If the request is to modify or continue an existing issue, do not create a duplicate.

## Rules

- Do not invent requirements, assignees, milestones, projects, or acceptance criteria.
- Labels: use a fitting existing label; if none fits, draft and create a new one after approval.
- Keep titles concise, ideally under 80 characters.
- Keep acceptance criteria observable, testable, and proportional.
- Add tests, docs, rollout, analytics, migrations, or follow-up work only when useful, not as boilerplate.
- For bugs, include repro, expected/actual behavior, and environment when known.
- Search for duplicates before creating; ask how to proceed if likely duplicates exist.
- Do not close, edit, or otherwise modify parent/source issues unless the user explicitly asks.
- For requested issue sets, prefer thin vertical slices that are independently buildable and verifiable over horizontal slices split only by implementation layer. A vertical slice is the smallest end-to-end behavior that can be implemented, verified, and reviewed independently.
- Prefer `AFK` slices. Mark `HITL` only when a real human decision, design review, product call, or architecture choice blocks implementation.

## Workflow

1. Preflight:

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If the target repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

2. Gather only missing essentials: repo, issue type, title/summary, completion criteria, bug repro details when relevant, and any explicit relationships between issues.

3. Choose structure:

   Use `templates/bug.md`, `templates/feature.md`, or `templates/task.md` by default. For approved implementation slices from a multi-issue breakdown, use `templates/vertical-slice.md`. Use repo templates only when requested.

4. Resolve metadata:

   ```bash
   gh api user --jq .login
   gh label list --limit 100
   gh issue list --search "<keywords>" --state all --limit 5
   ```

   Use mentioned assignees; otherwise use the current `gh` user. Select existing labels or draft new label metadata (`name`, `color`, `description`) when needed.

   If inspecting duplicate candidates, prefer REST when `gh issue view --comments` fails:

   ```bash
   repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
   gh api "repos/$repo/issues/<number>"
   gh api "repos/$repo/issues/<number>/comments" --paginate
   ```

5. Draft the issue. Show repo, title, body, assignee, labels/new labels, duplicate candidates, any milestone/project metadata, and any parent/sub-issue or blocking relationships. Ask for approval. For multiple issues from a plan or spec, use the multi-issue breakdown below before drafting final issue bodies.

6. After approval, create missing labels first, then create the issue:

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

   Add `--repo`, `--assignee`, repeated `--label`, `--milestone`, or `--project` only when resolved and approved.

   If creating multiple issues that should have parent/sub-issue or blocked-by relationships with one another, read `examples/multiple-related-issues.md` for the `gh api graphql` follow-up commands.

## Multi-Issue Breakdown

Use this path when the user asks to turn a plan, spec, PRD, or broad feature into multiple implementation issues.

1. Work from the current conversation. If the user gives an issue number, URL, or path as source material, fetch and read the full body and comments before breaking it down.
2. For implementation issue sets, briefly inspect relevant code, docs, and ADRs when available so titles and descriptions use the project's actual domain language. Skip this for simple one-off issues or when the user already provided enough concrete context.
3. Draft a complete issue set as vertical slices. Do not split into "backend", "frontend", or "tests" issues unless that is itself the smallest independently verifiable behavior.
4. Present the proposed breakdown as a numbered list. For each issue, show title, kind (`Tracking` or `Implementation`), type (`AFK` or `HITL` for implementation issues only), parent/source issue if any, blockers, user stories covered if the source material has them, and a short acceptance criteria summary.
5. Ask the user whether the granularity is right, the dependencies are correct, any slices should be merged or split, and the `AFK`/`HITL` markings are correct. Iterate until the user approves the breakdown.
6. After approval, publish blockers first, then dependents. Use `templates/vertical-slice.md` for implementation slices. Add `## Parent` and `## Blocked by` sections only when relevant. For dependent issue bodies, wait until blockers exist and use real issue URLs instead of placeholder titles. If the user requested parent/sub-issue, blocked-by, or blocking relationships, create the issues first, then read `examples/multiple-related-issues.md` and apply the `gh api graphql` follow-up commands. If a relationship command fails, report which relationships were not created and keep the textual issue links in the issue bodies.

## Output

Return the issue URL, title, assignee, labels, milestone/project metadata used, and any created parent/sub-issue or blocked-by relationships.

## Local References

- Templates: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, `templates/vertical-slice.md`
- Example: `examples/settings-crash-bug.md`
- Related issue example: `examples/multiple-related-issues.md`
