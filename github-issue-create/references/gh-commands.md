# GitHub Issue Commands

Load this reference only when exact `gh` commands, REST endpoints, or relationship verification are needed.

## Preflight

```bash
gh --version
gh auth status
gh repo view --json nameWithOwner --jq .nameWithOwner
```

If the repo is unclear, ask for `owner/name` and pass `--repo owner/name`.

## Draft Context

```bash
gh api user --jq .login
gh label list --limit 100
gh issue list --search "<keywords>" --state all --limit 5
```

If `gh issue view --comments` fails for source context:

```bash
repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
gh api "repos/$repo/issues/<number>"
gh api "repos/$repo/issues/<number>/comments" --paginate
```

## Create Issues

```bash
# If approved:
gh label create "<name>" --color "<hex>" --description "<description>"
gh issue create --title "<title>" --body-file "<approved-body-file>"
```

Add `--repo`, `--assignee`, repeated `--label`, `--milestone`, and `--project` only when resolved and approved.

## Native Relationships

Parent/sub-issue:

1. Identify the parent issue number.
2. Create or identify the child issue.
3. Resolve the child issue REST `id`.
4. Attach the child:

```bash
gh api \
  --method POST \
  "repos/$repo/issues/$parent_number/sub_issues" \
  -f sub_issue_id="$child_rest_id"
```

Blocked-by/blocking:

1. Identify the blocked issue number.
2. Create or identify the blocking issue.
3. Resolve the blocking issue REST `id`.
4. Attach the dependency:

```bash
gh api \
  --method POST \
  "repos/$repo/issues/$blocked_number/dependencies/blocked_by" \
  -f issue_id="$blocking_rest_id"
```

Verify sub-issues:

```bash
gh api "repos/$repo/issues/$parent_number/sub_issues"
```

Verify blockers:

```bash
gh api "repos/$repo/issues/$blocked_number/dependencies/blocked_by"
```

If an endpoint fails, report the exact command and error. Do not retry with different relationship semantics unless the user approves.
