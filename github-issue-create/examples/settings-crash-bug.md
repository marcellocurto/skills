# Example: Settings crash bug issue

## User context

```text
The settings page crashes when I click Save with an empty display name.
Expected: show validation error.
Actual: white screen.
Chrome on macOS.
```

## Drafted title

```text
Fix settings crash on empty display name
```

## Drafted body using `../templates/bug.md`

```markdown
## Summary

The settings page crashes when saving an empty display name instead of showing a validation error.

## Steps to Reproduce

1. Open the settings page.
2. Clear the display name field.
3. Click Save.

## Expected Behavior

A validation error is shown and the page remains usable.

## Actual Behavior

The page crashes to a white screen.

## Environment

- Browser: Chrome
- OS: macOS

## Severity / Impact

Users can crash the settings page while editing their profile.

## Acceptance Criteria

- [ ] Saving an empty display name shows a validation error instead of crashing.
- [ ] The settings page remains usable after the validation error is shown.
```

## Example command after approval

```bash
body_file="$(mktemp -t gh-issue-body.XXXXXX.md)"
cat > "$body_file" <<'EOF'
<drafted body here>
EOF

gh issue create \
  --title "Fix settings crash on empty display name" \
  --body-file "$body_file" \
  --assignee "$(gh api user --jq .login)" \
  --label "bug"

rm -f "$body_file"
```

Only include `--label "bug"` if `bug` exists in `gh label list` for the target repository.
