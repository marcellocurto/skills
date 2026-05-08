---
name: github-issue-quick-create
description: Quickly draft one straightforward GitHub issue with minimal metadata, ask only for missing essentials, and create it with `gh` after explicit approval.
---

# GitHub Issue Quick Create

Draft one straightforward GitHub issue, then create it with `gh` after explicit approval.

Use this for one simple bug, task, chore, or feature. Use `github-issue-create` for complex issue work.

## Goal

Give the user one usable issue draft with minimal metadata, then create it only after explicit approval.

## Success Criteria

- The user sees one clear draft with repo, title, body, and any explicit labels or assignees.
- The draft uses only details from the user, repository, or narrowly inspected code.
- Missing details are requested only when the draft would be unusable.
- No issue is created until the user explicitly approves the draft.
- The final response includes the issue number, title, and URL.

## Constraints

- Create only after explicit approval such as `create`, `ship it`, or `looks good, create it`.
- Handle exactly one issue.
- Do not search for duplicates unless the user explicitly asks.
- Ask for missing essentials before drafting.
- Use explicit metadata only. Do not infer labels, assignees, milestones, projects, priority, severity, or relationships.
- If the user provides a label or assignee, pass it to `gh issue create`; do not validate it up front unless needed.
- Do not create labels.
- Inspect code only when the user points at a file, function, failing test, stack trace, error, or repo-specific behavior.
- Keep code inspection narrow. Do not perform broad architecture discovery.

## Context And Tool Budget

Preflight `gh` before drafting or publishing:

```bash
gh --version
gh auth status
gh repo view --json nameWithOwner --jq .nameWithOwner
```

Use the current repo unless the user names another repo. If `gh` is missing, auth fails, or the repo cannot be resolved, stop and report the exact missing prerequisite.

Inspect only the minimum context needed to produce a usable issue. Search or read code only when a required title, behavior, repo fact, label/assignee, or acceptance criterion is missing.

If the user asks for duplicate search, run one targeted search using 2-4 distinctive terms and show likely matches before proceeding.

## Escalate To Full Issue Creation

Use `github-issue-create` instead when the request includes:

- Multiple issues, ticket breakdowns, epics, PRDs, specs, or implementation plans.
- Parent issues, sub-issues, blockers, dependencies, or native GitHub relationships.
- Duplicate search unless the user only wants a quick manual check for one issue.
- Label creation, milestone or project planning, broad metadata cleanup, tracer-bullet slicing, architecture decisions, or source issue decomposition.

## Essentials

Ask only for details that would make the draft unusable:

- Target repository, if `gh repo view` cannot resolve it.
- Issue type, if it is unclear whether this is a bug, task, chore, or feature.
- Expected outcome, if the request is too vague to title or verify.
- For bugs: expected and actual behavior, if either is missing.
- For tasks/features: at least one observable completion criterion, if none can be derived.

Do not ask for metadata, non-goals, rollout, analytics, tests, docs, or relationships unless the user mentions them.

## Draft Shape

Use a compact body. For most issues, include Summary and Acceptance Criteria sections.

For bugs with known reproduction details, include Summary, Reproduction, Expected, Actual, and Acceptance Criteria sections.

Show:

- Repo
- Title
- Full body under a Body: label
- Explicit labels/assignees only
- Duplicate results only if requested

Do not wrap the draft, body, metadata, duplicate results, or approval prompt in code fences.

End with: Reply "create" to create this issue, or tell me what to change.

## Publish

After approval, write the approved body to a temporary file and run `gh issue create --title "<title>" --body-file "$body_file"`. Add `--repo`, `--assignee`, and repeated `--label` only when explicit and approved. Remove the temporary file after creation.

If creation fails because provided metadata is invalid, report the exact failure and ask what to change. Do not retry with different metadata unless the user approves the change.

## Output

Return one line:

`#N - title - URL`

Include labels or assignees only if they were explicitly provided and successfully applied.

## Stop Rules

Stop after showing the draft and wait for approval. After publishing, stop once the created issue number, title, and URL are reported. Ask only when a missing essential would make the draft unusable.
