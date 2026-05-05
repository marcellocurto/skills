---
name: github-issue-create
description: Draft and create GitHub issues from user context using `gh issue create`. Use when asked to write, create, open, file, log, raise, or track an issue/ticket/bug; break down a PRD/spec/plan/epic into issues or tickets; create sub-issues; or split work into vertical slices. Draft first and create only after explicit approval.
---

# GitHub Issue Create

Draft and create GitHub issues with `gh`. Never create an issue before explicit approval. Do not duplicate existing issues or modify parent/source issues unless asked.

`AFK` = implementable end-to-end without human input. `HITL` = blocked on a human decision such as design, product, or architecture.

## Rules

- Use only facts from the user, repo, or fetched source issue. Do not invent requirements, labels, assignees, milestones, projects, or acceptance criteria.
- Use existing labels when possible; draft new labels only with approval.
- Keep titles under 80 characters when practical.
- Keep acceptance criteria observable and proportional.
- Add tests, docs, rollout, analytics, migrations, or follow-up work only when useful.
- For bugs, include repro, expected/actual behavior, environment, and impact when known.
- Search for duplicates and ask how to proceed if likely duplicates exist.
- For issue sets, use vertical slices: the smallest end-to-end behavior that can be implemented, verified, and reviewed independently. Avoid layer-only tickets unless the layer work is independently valuable.
- Prefer `AFK`; mark `HITL` only when implementation is blocked by a real human decision, design review, product call, or architecture choice.

## Workflow

1. Preflight:

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If `gh` is missing or auth fails, stop and tell the user to install `gh` or run `gh auth login`. If the repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

2. Resolve context and metadata:

   ```bash
   gh api user --jq .login  # default assignee when none is named
   gh label list --limit 100
   gh issue list --search "<keywords>" --state all --limit 5
   ```

   Ask only for missing essentials: repo, issue type, title/summary, completion criteria, bug repro details, and explicit relationships. Use mentioned assignees; otherwise use the current `gh` user. Choose duplicate-search keywords from 2-4 distinctive nouns in the title; if no hits, retry broader terms before concluding none exist. If high-similarity duplicates appear, show candidates and ask whether to use the existing issue, link it, or proceed. If the user provides a source issue number, URL, or path, fetch its full body and comments. For implementation issue sets, briefly inspect relevant code, docs, or ADRs when available so titles use project language.

   If `gh issue view --comments` fails, use REST:

   ```bash
   repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
   gh api "repos/$repo/issues/<number>"
   gh api "repos/$repo/issues/<number>/comments" --paginate
   ```

3. Draft for approval:

   Before drafting, read the relevant template: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, or `templates/vertical-slice.md`. Use repo templates when requested or when repo conventions clearly require them.

   For one issue, follow the template and show repo, title, body, assignee, labels/new labels, duplicate candidates, milestone/project metadata, and relationships.

   For multiple issues from a plan/spec, draft a numbered breakdown before final bodies. For each item show: title, kind (`Tracking` or `Implementation`), type (`AFK`/`HITL` for implementation only), parent/source, blockers, user stories covered when present, and acceptance summary. Ask whether granularity, dependencies, merge/split choices, and `AFK`/`HITL` markings are right. Iterate until approved. Use `templates/vertical-slice.md` for approved implementation slices.

   Present each draft with a repo/title header, fenced full body, metadata block (assignee, labels, new labels with color/description, milestone, project, parent, blocked-by, duplicate candidates), and end with: `Reply "create" to proceed, or tell me what to change.`

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

   Add `--repo`, `--assignee`, repeated `--label`, `--milestone`, and `--project` only when resolved and approved. For issue sets, publish blockers before dependents and use real issue URLs in `## Parent` and `## Blocked by`.

   If label creation fails, report the reason and ask whether to drop the label or retry. If multi-issue creation partially fails, list created URLs, uncreated issues, and pending relationships; do not retry destructively.

   If the user requested parent/sub-issue, blocked-by, or blocking relationships, create the issues first, then read `examples/multiple-related-issues.md` and run the `gh api graphql` follow-up commands. If a relationship command fails, report exactly which relationships were not created; keep textual issue links in the bodies.

## Output

Return one line per issue: `#N · title · URL · labels`. For multi-issue runs, add a relationships summary and any skipped metadata.

## References

- Templates: `templates/bug.md`, `templates/feature.md`, `templates/task.md`, `templates/vertical-slice.md`
- Examples: `examples/settings-crash-bug.md`, `examples/multiple-related-issues.md`
