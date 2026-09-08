---
name: close-ticket
description: Close the current ticket with a concise comment explaining the implementation.
disable-model-invocation: true
---

# Close Ticket

Identify the ticket being worked on or discussed in the conversation. Read it to confirm its identity and scope. If the intended ticket or its repository/project is unclear, stop and ask which ticket the user means. Do not guess from a branch name or choose among several plausible tickets.

Use the conversation and relevant implementation evidence to write one short comment explaining what changed, how it solves the ticket, and any verification actually performed. Include a relevant PR or commit link when available. Lead with the result, use plain language, and include only details that help someone understand the implementation. Skip process narration, boilerplate, and unsupported claims about tests, merging, or deployment. If completion cannot be established or required work remains, stop and explain the gap.

Post the comment, then close that ticket as completed using the available issue tracker tool or CLI. The request authorizes this comment and closure without another confirmation. Do not change unrelated ticket fields or close other tickets.

Verify that the comment was posted and the ticket is closed. If an operation fails or its result is uncertain, read the current state before retrying so the comment is not duplicated. Report any partial success accurately.

Return the ticket link and a brief confirmation.
