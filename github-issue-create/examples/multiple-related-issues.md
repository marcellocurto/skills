# Example: Multiple related issues

## User context

```text
Create issues for the import reliability work:
- Epic: Make CSV imports reliable.
- Task: Validate CSV headers before upload.
- Task: Add resumable import retries.
- The header validation task should be a sub-issue of the epic.
- The retry task should be a sub-issue of the epic.
- Retry work is blocked by header validation.
```

## Drafted breakdown and relationship plan

```text
Parent issue:
- Make CSV imports reliable (Type: HITL, Blocked by: None)

Vertical slices / sub-issues:
- Validate CSV headers before upload (Type: AFK, Parent: Make CSV imports reliable, Blocked by: None)
- Add resumable import retries (Type: AFK, Parent: Make CSV imports reliable, Blocked by: Validate CSV headers before upload)

Dependencies:
- Add resumable import retries is blocked by Validate CSV headers before upload
```

## Example commands after approval

Create all approved issues first and capture the issue URLs. The `*_body_file` variables are the approved issue body files from the normal workflow.

```bash
repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"

epic_url="$(gh issue create --repo "$repo" --title "Make CSV imports reliable" --body-file "$epic_body_file")"
headers_url="$(gh issue create --repo "$repo" --title "Validate CSV headers before upload" --body-file "$headers_body_file")"
retries_url="$(gh issue create --repo "$repo" --title "Add resumable import retries" --body-file "$retries_body_file")"
```

Resolve GitHub node IDs from the URLs:

```bash
epic_id="$(gh issue view "$epic_url" --repo "$repo" --json id --jq .id)"
headers_id="$(gh issue view "$headers_url" --repo "$repo" --json id --jq .id)"
retries_id="$(gh issue view "$retries_url" --repo "$repo" --json id --jq .id)"
```

Add the sub-issues:

```bash
for child_id in "$headers_id" "$retries_id"; do
  gh api graphql \
    -f query='
      mutation($parent: ID!, $child: ID!) {
        addSubIssue(input: { issueId: $parent, subIssueId: $child }) {
          issue { number url }
          subIssue { number url }
        }
      }' \
    -f parent="$epic_id" \
    -f child="$child_id"
done
```

Add the dependency. GitHub models this as "blocked issue is blocked by blocking issue":

```bash
gh api graphql \
  -f query='
    mutation($blocked: ID!, $blocking: ID!) {
      addBlockedBy(input: { issueId: $blocked, blockingIssueId: $blocking }) {
        issue { number url }
        blockingIssue { number url }
      }
    }' \
  -f blocked="$retries_id" \
  -f blocking="$headers_id"
```

For "A is blocking B", call `addBlockedBy` with `blocked=B` and `blocking=A`.
