---
name: github-issue-create
description: Turn provided context, notes, bugs, feature requests, or conversation history into a detailed GitHub issue and create it with `gh issue create`. Use when the user asks to write/create/open/file a GitHub issue, especially phrasing like "based on this, write a GitHub issue". The issue must have a concise title, detailed description, clear acceptance criteria, an assignee inferred from mentioned users or the current GitHub CLI user, and inferred labels.
---

# GitHub Issue Create

Create high-quality GitHub issues from the user's provided context, then file them with GitHub CLI.

## When to Use

Use this skill when the user asks to:

- Turn notes, bugs, feature requests, PR feedback, or conversation context into a GitHub issue
- Create/open/file a GitHub issue with `gh issue create`
- Write a concise issue title, detailed description, and acceptance criteria
- Infer labels for an issue from the issue content

## Core Requirements

Every issue must include:

1. **Concise title**: clear, specific, easily understandable, ideally under 80 characters.
2. **Detailed description**: explain the problem/opportunity, relevant context, expected behavior, and scope.
3. **Clear acceptance criteria**: use checkbox bullets that are observable and testable.
4. **Assignee**: assign to the user explicitly mentioned in the request; if no assignee is mentioned, default to the current GitHub CLI user from `gh api user --jq .login`.
5. **Labels**: infer appropriate labels from the issue content and available repository labels.
6. **Creation command**: create the issue with `gh issue create`.

## Workflow

### 1. Confirm there is enough context

If the request lacks enough information to create a useful issue, ask targeted follow-up questions before creating it. Do not invent core requirements.

Ask only for missing essentials, such as:

- What repository should this be filed in?
- Is this a bug, feature, task, documentation change, or refactor?
- What behavior should be accepted as complete?

If the repository is obvious from the current working directory and the context is sufficient, proceed without asking.

### 2. Determine the assignee

If the user explicitly mentions an assignee, use that GitHub username. Strip a leading `@` when passing it to `gh issue create`.

If no assignee is mentioned, use the currently authenticated GitHub CLI user:

```bash
gh api user --jq .login
```

If the current user cannot be determined, ask the user who should be assigned before creating the issue.

### 3. Inspect repository labels

Before choosing labels, check available labels:

```bash
gh label list --limit 100
```

Infer labels only after seeing the repository's actual labels. Do not assume common labels exist.

Map the issue content to whatever labels are available in the repository. For example, if labels like `bug`, `enhancement`, `documentation`, `refactor`, `tests`, `chore`, or `good first issue` appear in `gh label list`, use them only when they fit the issue content.

Do not create new labels unless the user explicitly asks. If no appropriate existing labels are available, create the issue without labels and mention that no matching labels were available.

### 4. Draft the issue body

Use a readable Markdown structure. Prefer this template unless the repo has its own issue template:

```markdown
## Description

<Explain the problem, feature, or task in detail. Include relevant context from the user request.>

## Why

<Explain the motivation, user impact, or value.>

## Scope

<Clarify what should be included. If helpful, also list explicit non-goals.>

## Acceptance Criteria

- [ ] <Observable/testable criterion>
- [ ] <Observable/testable criterion>
- [ ] <Observable/testable criterion>

## Notes

<Optional implementation notes, links, constraints, or open questions. Omit if unnecessary.>
```

Acceptance criteria must be specific enough that someone can verify whether the issue is complete.

### 5. Create the issue safely

Write the body to a temporary Markdown file to avoid shell escaping issues:

```bash
cat > /tmp/issue-body.md <<'EOF'
## Description

...
EOF
```

Then create the issue:

```bash
gh issue create \
  --title "<concise title>" \
  --body-file /tmp/issue-body.md \
  --assignee "<assignee-login>" \
  --label "<label-1>" \
  --label "<label-2>"
```

Use repeated `--label` flags for multiple labels. Omit `--label` flags if no suitable existing labels are available.

### 6. Report the result

After creation, return:

- The created issue URL from `gh issue create`
- The selected title
- The selected assignee
- The selected labels, if any

Keep the response brief.

## Quality Bar

Before running `gh issue create`, verify:

- [ ] The title is concise and understandable without extra context
- [ ] The body captures the user's actual request and does not add unsupported requirements
- [ ] Acceptance criteria are testable and outcome-focused
- [ ] Labels are inferred from available repository labels
- [ ] The issue is assigned to the mentioned user or, if none was mentioned, the current GitHub CLI user
