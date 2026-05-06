---
name: github-issue-quick-create
description: Quickly draft one straightforward GitHub issue with minimal metadata, ask only for missing essentials, and create it with `gh` after explicit approval.
---

# GitHub Issue Quick Create

Draft one straightforward GitHub issue with minimal ceremony, then create it with `gh` only after explicit approval.

Use this skill when the user wants to file one simple bug, task, chore, or feature issue and does not need issue architecture, duplicate research, relationships, projects, milestones, or rich metadata.

If the request is complex, use `github-issue-create` instead.

## Success Criteria

- The user sees one clear draft with repo, title, body, and any explicit labels or assignees.
- The draft contains only grounded details from the user, repository, or narrowly inspected code.
- Missing details are requested only when the issue would otherwise be unusable.
- No GitHub issue is created until the user explicitly approves the draft.
- The final response reports the created issue number, title, and URL.

## Rules

- Create only after explicit approval such as `create`, `ship it`, or `looks good, create it`.
- Handle exactly one issue.
- Ask for missing essentials before drafting.
- Do not search for duplicates unless the user explicitly asks.
- Do not infer labels, assignees, milestones, projects, priorities, severity, relationships, or new labels.
- Use explicit metadata only. If the user provides a label or assignee, pass it to `gh issue create`; do not validate it up front unless needed.
- Do not create labels.
- Inspect code only when the user points at a file, function, failing test, stack trace, error, or repo-specific behavior.
- Keep code inspection narrow. Do not perform broad architecture discovery.

## Escalate To Full Issue Creation

Use `github-issue-create` instead when the request includes:

- Multiple issues, ticket breakdowns, epics, PRDs, specs, or implementation plans.
- Parent issues, sub-issues, blockers, dependencies, or native GitHub relationships.
- Duplicate search unless the user only wants a quick manual check for one issue.
- Label creation, milestone/project planning, or broad metadata cleanup.
- Tracer-bullet slicing, architecture decisions, or source issue decomposition.

## Essentials

Ask concise follow-up questions only for details that would make the issue unusable:

- Target repository, if `gh repo view` cannot resolve it.
- Issue type, if it is unclear whether this is a bug, task, chore, or feature.
- One-sentence expected outcome, if the request is too vague to title or verify.
- For bugs: expected and actual behavior, if either is missing.
- For tasks/features: at least one observable completion criterion, if none can be derived.

Do not ask for labels, assignees, milestones, projects, severity, priority, non-goals, rollout, analytics, tests, docs, or relationships unless the user already mentions them.

## Workflow

1. Preflight:

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If `gh` is missing or auth fails, stop and report the fix. If the repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

2. Resolve only what is needed. Use the current repo unless the user named another repo. Resolve `assign me` with `gh api user --jq .login`. If the user explicitly asks for duplicate search, run one targeted `gh issue list --search "<2-4 distinctive terms>" --state all --limit 5`, show likely matches, and ask how to proceed.

3. Draft for approval:

   Use a compact body. For most issues:

   ```markdown
   ## Summary

   <One or two sentences describing the requested change.>

   ## Acceptance Criteria

   - [ ] <Observable completion criterion.>
   ```

   For bugs with known reproduction details:

   ```markdown
   ## Summary

   <Brief defect summary.>

   ## Reproduction

   <Steps, command, or scenario that shows the problem.>

   ## Expected

   <Expected behavior.>

   ## Actual

   <Actual behavior.>

   ## Acceptance Criteria

   - [ ] <The reproduction path now produces the expected behavior.>
   ```

   Show:

   - Repo
   - Title
   - Full body
   - Explicit labels/assignees only
   - Duplicate results only if requested

   End with: `Reply "create" to create this issue, or tell me what to change.`

4. Publish after approval. Write the approved body to a temporary file and run `gh issue create --title "<title>" --body-file "$body_file"`. Add `--repo`, `--assignee`, and repeated `--label` only when explicit and approved. Remove the temporary file after creation.

   If creation fails because provided metadata is invalid, report the exact failure and ask what to change. Do not retry with different metadata unless the user approves the change.

## Output

Return one line:

`#N - title - URL`

Include labels or assignees only if they were explicitly provided and successfully applied.
