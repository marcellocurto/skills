---
name: to-tickets
description: Turn approved work into well-scoped GitHub issues after checking for duplicates.
---

# To Tickets

Turn approved work into focused GitHub tickets. Each ticket is the only thing its implementer reads, so it must contain the whole task, what "done" means, and when to stop and ask.

Invoking this skill authorizes drafts only. Write nothing to GitHub until the user approves the drafts in step 4.

## Rules

- Use only what the user, the source material, and the repository tell you. Do not invent requirements, priorities, labels, relationships, or approval steps.
- Carry over decisions, constraints, rationale, edge cases, and research findings in enough detail that the implementer need not rediscover them. Keep specific constraints specific: "no pill-shaped buttons" stays as written rather than becoming "avoid a generic look".
- Mention confirmed code locations as starting points, not as scope.
- Leave out instructions like "think carefully" or "be thorough".
- Do not edit or close the source or parent issue unless the user asks.

## 1. Gather context

Read the source material and the code needed to make the tickets accurate. Ask only when the answer would change what a ticket requires, how the work is split, or its order.

Take the target repository as `HOST/OWNER/REPO` from the user or the local remote, and use that host for every GitHub read and write.

For pull-request feedback, fetch threads with `python3 "<skill-path>/scripts/fetch_review_context.py"` or a connector, check each unresolved thread against current code, and ticket only concerns that still need work.

List the repository's labels and learn their meaning from descriptions and past use, not names alone. Assume an agent with this repository's usual setup will implement the tickets, unless the user or repository says otherwise.

## 2. Check for duplicates

Search open and closed issues for each planned outcome using plain-language terms. Compare goals and scope, not titles. Report likely duplicates with URLs and the overlap, and do not change or reuse an existing issue without approval. If the search fails, create nothing until it works or the user says to proceed without it.

## 3. Draft the tickets

### Split the work

Keep work in one ticket when it produces one useful result that can be reviewed as a whole. Split only when parts can finish independently, need different owners, or must happen in order to avoid a real risk. A feature ticket covers every layer the feature needs.

Mark a ticket blocked by another only when it cannot be completed without it; preferred order is not a blocker. When replacing an interface whose callers cannot all change at once, write ordered tickets to add the new interface, move callers, and remove the old one.

Write research tickets only when the user asks for discovery. Do not create tracking or epic issues to group the set, and attach tickets to an existing parent only when the user or repository convention requires it.

### Separate human work

Decisions, approvals, and actions that need a person go in their own ticket with a clear completion signal and the repository's human-work label. A person owns this work even if an agent could operate the interface. Do not create tickets for ordinary PR review.

- A human action the implementation needs first blocks the implementation ticket.
- Human approval of finished work is blocked by the implementation ticket, which must not list that approval as a completion condition.
- Approval needed before rollout blocks the rollout work.

### Write each ticket

Write for a developer who has not followed the discussion. Use simple, everyday words, with technical terms only where they name something exactly, such as a file, command, or API.

Title: the outcome in simple words that is understandable without opening the ticket, such as "Retry failed webhook deliveries with backoff" rather than "Webhook improvements".

Body, in this order:

```markdown
## Summary

Two to four sentences: what needs to change, why, and who is affected. A reader who stops here should know what the ticket asks for.

## Current behavior

What happens today, or the research findings for new work. Keep verified facts apart from guesses.

## Desired outcome

The behavior when the work is done. State confirmed requirements as requirements and optional ideas as tradeoffs. Do not prescribe implementation the source has not decided.

## Acceptance criteria

Plain bullets that together mean done, so the implementer works until all hold and then stops. Include required end states, such as deleted code or no remaining callers, and the full scope, such as "every payment endpoint". Name a test suite or command only when it is the evidence that matters. No implementation steps, generic "tests pass" lines, or checkboxes.

## Stop and ask

Situations specific to this ticket where continuing needs a decision the ticket does not make, such as finding a caller outside this repository.

## Execution requirements

Tools, access, or fixtures beyond the repository's usual setup.

## Risks and non-goals

What could break, and what this ticket deliberately does not do.

## Context

Links to the source discussion and related issues, and code locations to start from.
```

Always include Summary, Desired outcome, and Acceptance criteria. Include the others only when they have real content. Never write a section that says "None".

For each acceptance criterion, decide who can verify it and with what evidence. Never weaken the evidence to fit the available tools. A capability missing from the environment is a gap to report, not a reason to make the work human-owned.

### Choose labels

Use existing labels only, and add priority or workflow labels only when repository convention supports them. If a needed label is missing, leave it off and say so. Never use a `blocked` label.

Apply `ready-for-agent` when an agent in the intended environment can finish and verify the ticket from its text alone, with no human step inside the ticket and no stop condition already known to apply. A **Stop and ask** section lists situations that would need a decision if they arise; it does not make the ticket unready. Never apply the label to research, decision, or human-owned tickets. A blocked-by relationship is not a step inside the ticket, so a ready ticket keeps the label while that relationship holds it.

## 4. Get approval

Show the repository, each ticket's exact title and body, labels with a short reason (including for `ready-for-agent`), relationships, and duplicate findings. Wait for the user to approve these drafts. A request for tickets, approval of the underlying plan, or an instruction to run several skills in a row is not approval. Approval carries over when resuming an unchanged set; material changes need new approval.

## 5. Publish

Before any write, search the repository's open issues for each approved title and reuse any that this set already created. Never create a ticket twice, and never delete, reopen, or overwrite an issue to retry a step.

Use `gh` for all writes. Confirm every approved label exists; if one does not, ask instead of creating or substituting it. Then work in three phases, because a relationship needs both issue numbers:

1. Create every issue with `gh issue create --body-file`, blockers before the tickets they block.
2. Add exactly its approved labels to each issue.
3. Add each approved relationship with the bundled helper, which resolves and verifies database IDs:
   - parent: `python3 "<skill-path>/scripts/set_issue_relationship.py" --repo HOST/OWNER/REPO --parent PARENT --sub-issue CHILD`
   - blocked by: `python3 "<skill-path>/scripts/set_issue_relationship.py" --repo HOST/OWNER/REPO --blocked BLOCKED --blocked-by BLOCKER`

Both numbers must belong to the named repository; for a cross-repository relationship, use `gh api` with each issue's database ID. If a relationship fails, never fall back to a label or body link.

## 6. Report

Read back every issue, label, and relationship. Return the issue URLs and relationship status. If anything is incomplete, say what worked, what is left, and the exact error.
