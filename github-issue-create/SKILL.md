---
name: github-issue-create
description: Draft and create GitHub issues from user context using `gh issue create`. Use when asked to write, create, open, file, log, raise, or track an issue/ticket/bug in GitHub. Draft first and create only after explicit approval.
---

# GitHub Issue Create

Create one or more GitHub issues from the user's context. Draft first; run `gh issue create` only after explicit approval. If the request is to modify or continue an existing issue, do not create a duplicate.

## Rules

- Use the target repo's templates, labels, and conventions when available.
- Do not invent requirements, labels, assignees, milestones, projects, or acceptance criteria.
- Use only labels returned by `gh label list`.
- Keep titles concise, ideally under 80 characters.
- Keep acceptance criteria observable, testable, and proportional to the user's input.
- Do not add tests, docs, rollout, analytics, migrations, or follow-up work unless requested or required by the repo template.
- For bugs, anchor the issue in repro, expected behavior, actual behavior, and environment when available.
- Search for duplicates before creating; if likely duplicates exist, ask whether to stop, update, or continue.

## Workflow

1. Preflight:

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If the target repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

2. Gather only missing essentials: repo, issue type, title/summary, completion criteria, and bug repro details when relevant.

3. Choose structure:

   ```bash
   find .github/ISSUE_TEMPLATE -maxdepth 1 -type f 2>/dev/null
   ```

   Prefer matching repo templates. Otherwise use `templates/bug.md`, `templates/feature.md`, or `templates/task.md`.

4. Resolve metadata:

   ```bash
   gh api user --jq .login
   gh label list --limit 100
   gh issue list --search "<keywords>" --state all --limit 5
   ```

   Use mentioned assignees; otherwise use the current `gh` user. Omit labels when none match.

   If inspecting duplicate candidates, prefer REST when `gh issue view --comments` fails:

   ```bash
   repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
   gh api "repos/$repo/issues/<number>"
   gh api "repos/$repo/issues/<number>/comments" --paginate
   ```

5. Draft the issue. Show repo, title, body, assignee, labels, duplicate candidates, and any milestone/project metadata. Ask for approval. For multiple issues, draft all first, then create sequentially after approval.

6. Create after approval using a temp body file:

   ```bash
   body_file="$(mktemp -t gh-issue-body.XXXXXX.md)"
   cat > "$body_file" <<'EOF'
   <approved issue body>
   EOF
   gh issue create --title "<title>" --body-file "$body_file"
   rm -f "$body_file"
   ```

   Add `--repo`, `--assignee`, repeated `--label`, `--milestone`, or `--project` only when resolved and approved.

## Output

Return the issue URL, title, assignee, labels, and milestone/project metadata used.

## Local References

- Templates: `templates/bug.md`, `templates/feature.md`, `templates/task.md`
- Example: `examples/settings-crash-bug.md`
