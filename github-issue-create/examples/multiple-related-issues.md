# Example: Multiple related issues

## User context

```text
Create issues for import reliability:
- Tracking issue: Make CSV imports reliable.
- Sub-issues: validate CSV headers; add resumable import retries.
- Retry work is blocked by header validation.
- User story: as an operator, I can recover from import problems without restarting manually.
```

## Drafted breakdown

```text
1. Make CSV imports reliable
   - Kind: Tracking
   - Blocked by: None
2. Validate CSV headers before upload
   - Kind: Implementation
   - Type: AFK
   - Parent: Make CSV imports reliable
   - End-to-end behavior: invalid CSV headers fail before upload work starts.
   - Demo / verification path: upload a CSV with missing headers and verify actionable errors.
   - Blocked by: None
   - Tracer-bullet: yes - validation runs from upload path to user-facing error.
   - Acceptance summary: invalid or missing headers produce actionable errors
3. Add resumable import retries
   - Kind: Implementation
   - Type: AFK
   - Parent: Make CSV imports reliable
   - End-to-end behavior: failed imports resume without manual restart.
   - Demo / verification path: interrupt an import, retry it, verify it resumes from the last safe point.
   - Blocked by: Validate CSV headers before upload
   - Tracer-bullet: yes - retry behavior runs through import state and operator workflow.
   - Acceptance summary: failed imports resume from the last safe point
```

## Example commands after approval

Create approved issues and capture URLs. `*_body_file` variables come from the normal workflow.

```bash
repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"

epic_url="$(gh issue create --repo "$repo" --title "Make CSV imports reliable" --body-file "$epic_body_file")"
headers_url="$(gh issue create --repo "$repo" --title "Validate CSV headers before upload" --body-file "$headers_body_file")"
retries_url="$(gh issue create --repo "$repo" --title "Add resumable import retries" --body-file "$retries_body_file")"
```

Resolve numbers and REST IDs:

```bash
epic_number="${epic_url##*/}"
headers_number="${headers_url##*/}"
retries_number="${retries_url##*/}"

headers_id="$(gh api "repos/$repo/issues/$headers_number" --jq .id)"
retries_id="$(gh api "repos/$repo/issues/$retries_number" --jq .id)"
```

Add the sub-issues:

```bash
for child_id in "$headers_id" "$retries_id"; do
  gh api \
    -X POST \
    "repos/$repo/issues/$epic_number/sub_issues" \
    -f sub_issue_id="$child_id"
done
```

Add the dependency:

```bash
gh api \
  -X POST \
  "repos/$repo/issues/$retries_number/dependencies/blocked_by" \
  -f issue_id="$headers_id"
```

Verify:

```bash
gh api "repos/$repo/issues/$epic_number/sub_issues" --jq '.[].number'
gh api "repos/$repo/issues/$retries_number/dependencies/blocked_by" --jq '.[].number'
```

For "A is blocking B", add a blocked-by relationship on B with A's REST issue `id`.
