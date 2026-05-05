# Example: Tracer-bullet breakdown

## User context

```text
Break down notification preferences:
- Users can opt out of marketing emails.
- Users can opt out of product update emails.
- Admins can see when a preference changed.
```

## Bad: horizontal layers

Do not use this shape:

```text
1. Add notification preference database fields
2. Build notification preference API
3. Build settings UI
4. Add tests
```

No issue is demoable alone.

## Good: tracer bullets

```text
1. Let users opt out of marketing emails
   - Kind: Implementation
   - Type: AFK
   - End-to-end behavior: user disables marketing email; marketing sends exclude them.
   - Demo / verification path: toggle setting, reload it, inspect/send marketing email, verify exclusion.
   - Blocked by: None
   - Tracer-bullet: yes - preference works from UI through send path.
   - Acceptance summary: preference persists; UI reflects it; send path checks it; tests cover behavior.

2. Let users opt out of product update emails
   - Kind: Implementation
   - Type: AFK
   - End-to-end behavior: user disables product updates; product sends exclude them.
   - Demo / verification path: toggle setting, reload it, inspect/send product update, verify exclusion.
   - Blocked by: marketing opt-out, if it establishes the shared preference path.
   - Tracer-bullet: yes - second preference works through the same path.
   - Acceptance summary: preference persists; UI reflects it; send path checks it; tests cover behavior.

3. Show admins preference change history
   - Kind: Implementation
   - Type: AFK
   - End-to-end behavior: admin sees preference changes in audit history.
   - Demo / verification path: change preference, open admin audit view, verify change appears.
   - Blocked by: first preference slice that emits audit events.
   - Tracer-bullet: yes - change flows from user action to admin audit view.
   - Acceptance summary: event records who/what/when; admin view shows it; tests cover audit path.
```

First slice may include minimal schema, API, UI, send-path, and tests. Later slices reuse or extend it. Do not create separate layer tickets.
