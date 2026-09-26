---
name: to-tickets
description: Turn approved work into well-scoped GitHub issues after checking for duplicates and dependencies.
---

# To Tickets

Turn approved work into focused GitHub tickets. Each ticket is the only thing its implementer reads, so it must contain the whole task, what "done" means, and when to stop and ask.

Invoking this skill, even after `implementation-planner`, authorizes drafts only. Write nothing to GitHub until the user approves the drafts in step 4.

## Rules

- Use only what the user, the source material, and the repository tell you. Do not invent requirements, priorities, labels, relationships, or approval steps.
- Keep decisions, constraints, rationale, edge cases, and research findings in enough detail that the implementer need not rediscover them. Mention confirmed code locations as starting points, not as scope.
- For interface work, carry over each visual pattern the source rules out, by name ("no pill-shaped buttons"). Do not reduce them to "avoid a generic look".
- Leave out instructions like "think carefully" or "be thorough".
- Do not edit or close the source or parent issue unless the user asks.

## 1. Gather context

Read the source material and the code needed to make the tickets accurate. Ask only when the answer would change what a ticket requires, how the work is split, or its order.

For pull-request feedback, fetch threads with `python "<skill-path>/scripts/fetch_review_context.py"` or a connector, check each unresolved thread against current code, and ticket only concerns that still need work.

List the repository's labels and learn their meaning from descriptions and past use, not names alone. Find out which environment will implement the tickets and what tools, access, and permissions it has; it may differ from this session.

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

Use a specific title that names the outcome, and plain technical language. State confirmed requirements as requirements and optional ideas as tradeoffs. Use only sections that add something; a simple ticket may need only a summary, desired outcome, and acceptance criteria. Choose from `## Summary`, `## Why this issue exists`, `## Current behavior` or `## Research and findings`, `## Impact`, `## Desired outcome`, `## Acceptance criteria`, `## Stop and ask`, `## Execution requirements`, `## Risks / non-goals`, and `## Context` (last). Keep verified facts apart from guesses, and do not prescribe implementation the source has not decided.

- `## Acceptance criteria` is the finish line: plain bullets that together mean done, so the implementer works until all hold and then stops. Include required end states such as deleted code or no remaining callers, and state the full scope ("every payment endpoint"). Name a test suite or command only when it is the evidence that matters. Leave out implementation steps, generic "tests pass" lines, and checkboxes.
- `## Stop and ask` lists situations specific to this ticket where continuing needs a decision the ticket does not make, such as finding a caller outside this repository.
- `## Execution requirements` lists tools, access, or fixtures beyond the repository's usual agent setup.

For each criterion, decide who can verify it and with what evidence. Never weaken the evidence to fit the available tools. A capability that is missing from the environment is a gap to report, not a reason to make the work human-owned.

### Choose labels

Use existing labels only, and add priority or workflow labels only when repository convention supports them. If a needed label is missing, leave it off and say so. Never use a `blocked` label.

Apply `ready-for-agent` when an agent in the intended environment can finish and verify the ticket from its text alone, with no human step and no known stop condition. Never apply it to research, decision, or human-owned tickets. A ready ticket keeps the label while a blocked-by relationship holds it.

## 4. Get approval

Show the repository, each ticket's exact title and body, labels with a short reason (including for `ready-for-agent`), relationships, and duplicate findings. Wait for the user to approve these drafts. A request for tickets, approval of the underlying plan, or an instruction to run several skills in a row is not approval. Approval carries over when resuming an unchanged set; material changes need new approval.

## 5. Publish

Before any write, read back what this set already created and reuse it. Never create a ticket twice, and never delete, reopen, or overwrite an issue to retry a step.

Use `gh` for all writes. Take `HOST/OWNER/REPO` from the user or the local remote and use that host throughout. Confirm every approved label exists; if one does not, ask instead of creating or substituting it. Then, creating blockers first:

1. Create each issue with `gh issue create --body-file`.
2. Add exactly its approved labels.
3. Add each approved relationship with the bundled helper, which resolves and verifies database IDs:
   - parent: `python "<skill-path>/scripts/set_issue_relationship.py" --repo HOST/OWNER/REPO --parent PARENT --sub-issue CHILD`
   - blocked by: `python "<skill-path>/scripts/set_issue_relationship.py" --repo HOST/OWNER/REPO --blocked BLOCKED --blocked-by BLOCKER`

Both numbers must belong to the named repository; for a cross-repository relationship, use `gh api` with each issue's database ID. If a relationship fails, never fall back to a label or body link.

## 6. Report

Read back every issue, label, and relationship. Return the issue URLs and relationship status. If anything is incomplete, say what worked, what is left, and the exact error.
