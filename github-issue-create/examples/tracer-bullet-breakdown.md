# Example: Tracer-bullet breakdown

## User context

```text
Break down notification preferences:
- Users can opt out of marketing emails.
- Users can opt out of product update emails.
- Admins can see when a preference changed.
```

## Bad horizontal breakdown

Do not create this shape unless the user explicitly asks for layer work:

```text
1. Add notification preference database fields
2. Build notification preference API
3. Build settings UI
4. Add tests
```

Each issue depends on the others before any behavior is demoable. This is not independently grabbable.

## Good tracer-bullet breakdown

```text
1. Let users opt out of marketing emails
   - Kind: Implementation
   - Type: AFK
   - End-to-end behavior: a user toggles marketing emails off and marketing sends respect it.
   - Demo / verification path: toggle the setting, reload it, trigger or inspect a marketing send path, and verify the user is excluded.
   - Blocked by: None
   - Acceptance summary: preference persists, UI reflects it, send path checks it, tests cover the behavior.

2. Let users opt out of product update emails
   - Kind: Implementation
   - Type: AFK
   - End-to-end behavior: a user toggles product updates off and product update sends respect it.
   - Demo / verification path: toggle the setting, reload it, trigger or inspect a product update send path, and verify the user is excluded.
   - Blocked by: Let users opt out of marketing emails, if it establishes the shared preference pattern
   - Acceptance summary: preference persists, UI reflects it, send path checks it, tests cover the behavior.

3. Show admins preference change history
   - Kind: Implementation
   - Type: AFK
   - End-to-end behavior: when a user changes a notification preference, admins can see the change in the audit view.
   - Demo / verification path: change a preference as a user, open the admin audit view, and verify the change is visible.
   - Blocked by: first preference slice that emits the audit event
   - Acceptance summary: event is recorded, admin view shows who changed what and when, tests cover the audit path.
```

The first slice may include the minimal schema, API, UI, send-path, and test work needed for marketing opt-out. Later slices reuse or extend that path instead of creating separate layer tickets.
