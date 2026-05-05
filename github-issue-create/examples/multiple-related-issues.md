# Example: Multiple related issues

## User context

```text
Create issues for import reliability:
- Tracking issue: Make CSV imports reliable.
- Sub-issues: validate CSV headers; add resumable import retries.
- Retry work is blocked by header validation.
- User story: as an operator, I can recover from import problems without restarting manually.
```

## Drafted breakdown and relationship plan

```text
1. Make CSV imports reliable
   - Kind: Tracking
   - Blocked by: None
2. Validate CSV headers before upload
   - Kind: Implementation
   - Type: AFK
   - Parent: Make CSV imports reliable
   - Blocked by: None
   - User stories covered: detect import problems before upload work starts
   - Acceptance summary: invalid or missing headers produce actionable errors
3. Add resumable import retries
   - Kind: Implementation
   - Type: AFK
   - Parent: Make CSV imports reliable
   - Blocked by: Validate CSV headers before upload
   - User stories covered: recover from import problems without restarting manually
   - Acceptance summary: failed imports resume from the last safe point
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
