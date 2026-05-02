---
name: github-issue-create
description: Create detailed new GitHub issues from context using `gh issue create`. Use when asked to write/create/open/file/log/raise an issue, open a ticket, log a bug, file this, or track something in GitHub.
---

# GitHub Issue Create

Create new GitHub issues from user context. Draft first; run `gh issue create` only after explicit approval. If the user wants to modify an existing issue, do not create a duplicate.

## Requirements

- Title: concise, clear, ideally under 80 characters.
- Body: use repo issue template when available; otherwise use `templates/bug.md`, `templates/feature.md`, or `templates/task.md`.
- Acceptance criteria: observable, testable, and derived only from the user's input.
- Assignee: mentioned GitHub user, otherwise current `gh` user.
- Labels: use only labels that exist in the target repo.

## Workflow

1. **Preflight**

   ```bash
   gh --version
   gh auth status
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```

   If not in the target repo, ask for `owner/name` and use `--repo owner/name` in all `gh` commands.

2. **Ask only for missing essentials**

   Get the target repo, issue type, and completion criteria if unclear. For bugs, get repro steps, expected behavior, actual behavior, and environment when missing. Do not invent requirements.

3. **Choose issue structure**

   ```bash
   find .github/ISSUE_TEMPLATE -maxdepth 1 -type f 2>/dev/null
   ```

   Prefer matching repo templates, including YAML issue forms. If none apply, use:
   - `templates/bug.md` for defects/regressions/repro-based issues
   - `templates/feature.md` for user-facing enhancements
   - `templates/task.md` for chores/docs/refactors/tests/maintenance

4. **Resolve assignee, labels, duplicates**

   ```bash
   gh api user --jq .login
   gh label list --limit 100
   gh issue list --search "<keywords>" --state all --limit 5
   ```

   - Use a mentioned assignee, stripping leading `@`; otherwise use the current `gh` user.
   - Infer labels only from the actual `gh label list` output; never assume common labels exist or create labels unless asked.
   - If likely duplicates appear, show them and ask whether to continue, update an existing issue, or stop.

5. **Draft carefully**

   - Keep the body grounded in the user's content.
   - Keep acceptance criteria proportional: if the user gave 3 concrete bullets, usually produce ≤3 criteria.
   - Do not add tests, docs, rollout, analytics, monitoring, migration, or follow-up work unless requested or required by the repo template.
   - For bugs, criteria should normally state that the original repro now produces the expected behavior. Add regression-test criteria only when requested or clearly expected by repo norms.
   - Omit `Why` if it duplicates the description.

6. **Confirm before create**

   Show repo, title, body, assignee, labels, optional milestone/project metadata, and duplicate candidates. Ask for approval. For multiple issues, draft all first, get one combined approval, then create sequentially.

7. **Create safely**

   Use `mktemp`; do not use a fixed temp path. Keep `<<'EOF'` quoted so user content is not shell-expanded.

   ```bash
   body_file="$(mktemp -t gh-issue-body.XXXXXX.md)"
   cat > "$body_file" <<'EOF'
   <approved issue body>
   EOF

   gh issue create \
     --title "<title>" \
     --body-file "$body_file" \
     --assignee "<assignee>" \
     --label "<label>"

   rm -f "$body_file"
   ```

   Repeat `--label` for multiple labels; omit labels if none match. Add `--repo`, `--milestone`, or `--project` only when needed/requested.

## Response

Return the issue URL prominently, plus title, assignee, labels, and any milestone/project metadata used.

## References

- Templates: [bug](templates/bug.md), [feature](templates/feature.md), [task](templates/task.md)
- Example: [settings crash bug](examples/settings-crash-bug.md)
