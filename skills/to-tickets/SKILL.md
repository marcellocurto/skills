---
name: to-tickets
description: Turn approved work into well-scoped GitHub issues after checking for duplicates and dependencies.
---

# To Tickets

Turn existing context into one or more focused GitHub tickets that can be implemented and verified independently.

## Principles

- Use facts from the user, source material, and repository. Do not invent requirements, goals, metadata, relationships, or priority.
- Preserve requirements, constraints, decisions, rationale, meaningful edge cases, and verified findings from prior research. Do not compress away technical detail that would force the implementation agent to repeat exploration.
- Make each ticket self-contained enough to complete without reading a parent or sibling. Reference relevant existing specs, ADRs, or repository docs when they exist; do not require or invent one.
- Keep cohesive work together. Do not split a useful ticket merely to make it smaller.
- Split only when a ticket has become too broad to implement or review coherently, contains outcomes that can deliver value independently, or needs safety-driven sequencing. When splitting feature work, prefer end-to-end slices that include every layer needed for the behavior without inventing work.
- Declare only genuine blocking dependencies. Sequence or preference alone is not a blocker.
- Do not modify or close a source or parent issue unless the user explicitly asks.
- Avoid generic file inventories and speculative code paths. Include confirmed code locations as current starting points when they save meaningful exploration, but do not present them as authoritative scope.

## GitHub access

- Use `gh` for issue creation, labels, native relationships, and verification.
- When a GitHub connector is already available, it may be used for repository, issue, pull-request, or review-thread reads. Use `gh` for all writes in one publication; do not mix connector and CLI writes.
- Resolve the exact `OWNER/REPO` from an explicit identifier or the local remote. Ask only when the repository remains ambiguous after local inspection.
- Before any `gh` operation, require the CLI and confirm `gh auth status`. If authentication fails, ask the user to run `gh auth login`.

## Process

### 1. Gather context

Work from the conversation and any referenced plan, spec, issue, comments, repository documentation, ADRs, domain glossary, or prior research. Inspect the codebase only as needed to make the tickets accurate. Ask only when unresolved ambiguity would materially change the ticket set, semantics, or dependency graph.

When the user explicitly asks to turn pull-request feedback into tickets, retrieve thread-aware review context through an available connector or `python "<skill-path>/scripts/fetch_review_context.py"`. Treat unresolved, non-outdated threads as candidates, but check them against the current code: unresolved feedback may already be addressed. Consult resolved, outdated, duplicate, top-level, and review-summary comments only as needed for context or unthreaded actionable feedback. Do not create implementation tickets for feedback that is already addressed, not actionable, or unclear; surface the disposition and use a research or decision ticket only when that outcome is itself explicitly requested.

List the repository's existing labels with their descriptions. Use descriptions and established usage on comparable issues to understand the repository's label vocabulary; do not infer semantics from a label name alone when its meaning is ambiguous.

### 2. Check for duplicates

Before drafting new tickets, search both open and closed issues for likely duplicates of each intended outcome. Use the plan's plain-language concepts rather than relying on one exact title. Read plausible matches closely enough to compare their actual goals and scope.

Surface likely duplicate URLs and explain the overlap. Do not treat a similar title as proof of duplication, and do not modify, close, or reuse an existing issue without the user's approval. If the search cannot run, report why; do not publish until it succeeds or the user explicitly approves proceeding without it.

### 3. Draft the ticket set

Write each ticket as a compact argument that lets a busy maintainer understand the situation, judge its importance, and act without reconstructing the surrounding conversation. Use simple technical language and a specific, outcome-oriented title that makes sense on its own. Avoid shorthand, clever wording, and jargon that does not improve precision.

Use only sections that add information. A simple ticket may need only a summary, desired outcome, and acceptance criteria; omit empty sections and do not create both a simple summary and a second summary. Choose from these sections as the work requires:

- `## Summary`: explain in a short paragraph what is currently true, why it matters, and what should happen next; do not merely restate the title
- `## Why this issue exists`: when the ticket is derived from other work or needs justification as a separate unit, explain why it is distinct and worthwhile rather than only naming its source or classification
- `## Evidence` or `## Current behavior`: record verified observations, relevant code locations, constraints, and decisions; distinguish confirmed facts from hypotheses
- `## Impact`: state the concrete user, operational, or maintenance consequence and calibrate urgency honestly, including when the work is non-blocking or protects only against a future regression
- `## Desired outcome`: describe what should become true without prescribing files, code, or implementation details unless the source material already decided them
- `## Acceptance criteria`: use ordinary bullets describing independently verifiable behavior; do not use task-list checkboxes, implementation steps, code locations, generic “tests pass” statements, or bullets that merely restate the desired outcome
- `## Research and findings`: use this instead of a basic evidence section when prior exploration is substantial, preserving rejected approaches, pitfalls, and technical detail that would otherwise have to be rediscovered
- `## Risks / non-goals`: capture meaningful compatibility risks, scope boundaries, and nearby work that must remain untouched; omit generic boilerplate
- `## Context`: place source issues, pull requests, specifications, ADRs, and other provenance at the end so they support rather than interrupt the issue

Add another section only when important maintainer-facing information does not fit these concepts. Calibrate the language to the status of the work: state confirmed requirements directly, but present optional suggestions as tradeoffs rather than pretending implementation has already been decided. When the honest outcome is a maintainer decision, state the decision and evidence needed and allow the suggestion to be closed with a clear rationale.

Prefer cohesive, independently useful vertical slices with enough scope and context to act on. A ticket set may contain exactly one issue. Split only when the resulting tickets are easier to execute, verify, or sequence—not to meet an arbitrary size target. Allow enabling work, migrations, infrastructure, and mechanical refactors when those are the honest units of work. For a genuinely wide migration, describe the expand, consumer-migration, and old-path-removal stages in that order.

Allow research or investigation tickets when discovery is itself explicitly requested, independently useful work with a concrete question and completion signal. When the user asks for an actionable implementation ticket set for a feature believed to be ready, resolve material unknowns before drafting; do not turn them into research tickets that postpone implementation.

Do not create a tracking, overview, epic, or coordination issue merely to organize the set or preserve shared context. Attach tickets to an existing parent only when the user explicitly requests it or established repository convention requires it.

Let consumer and rollout evidence determine how an interface replacement is ticketed. When one coordinated change controls every consumer, keep the replacement cohesive and remove the old path in that ticket. When compatibility or rollout constraints require overlap, split the work into introduction, consumer migration, and removal. Record the removal condition for each temporary adapter and include the final cleanup ticket. Do not assume an interface is internal or invent a branching strategy without evidence.

Choose the smallest useful set of existing labels for each ticket. Select labels that accurately describe its type, affected area, or other established repository dimensions. Add priority, workflow, or ownership labels only when the source material and repository convention support them. Do not invent labels, force a label from an unsuitable taxonomy, or apply labels merely because their names share words with the ticket. If no existing label fits, leave that dimension unlabeled and surface the taxonomy gap.

Treat `ready-for-agent` as a readiness state, not a default ticket category. Apply it only when all of the following are true:

- the ticket calls for a concrete implementation or repository change, rather than research as its outcome
- the relevant decisions, constraints, context, and completion signals are sufficient to begin
- the work specified by the ticket does not depend on live human judgment, conversation, approval, access provisioning, or manual action

Do not apply `ready-for-agent` to research, investigation, discovery, or spike tickets; decision or coordination work; human-owned tasks; or underspecified implementation. Normal codebase exploration needed while implementing a well-specified change does not by itself make a ticket a research task.

Treat readiness and dependency status as separate dimensions. A fully specified, agent-executable ticket may carry `ready-for-agent` while an open native blocked-by relationship prevents it from starting. Represent that dependency only with the native relationship; do not withhold `ready-for-agent` merely because the ticket is blocked.

Present the exact drafts, duplicate candidates, proposed native relationships, and labels, with a short rationale for each ticket's proposed labels and for including or omitting `ready-for-agent`.

Wait for explicit approval before creating anything. Approval of the drafts includes approval for their listed labels and native relationships.

### 4. Publish

Preflight `gh`, authentication, the repository, and every approved label. If an approved label is missing, report it and ask before creating anything; do not create or silently substitute a label. Use `gh issue create` with a body file so Markdown and real newlines are preserved.

Create approved blockers before their dependents, then:

- create each approved issue
- apply exactly the approved labels for that issue
- create approved parent/sub-issue relationships with GitHub's native relationship
- create approved blocked-by/blocking relationships with GitHub's native relationship

For native relationships, run the bundled helper after both issues exist. It retrieves the required database IDs and verifies the relationship:

- parent: `python "<skill-path>/scripts/set_issue_relationship.py" --repo OWNER/REPO --parent PARENT_NUMBER --sub-issue CHILD_NUMBER`
- blocked by: `python "<skill-path>/scripts/set_issue_relationship.py" --repo OWNER/REPO --blocked BLOCKED_NUMBER --blocked-by BLOCKER_NUMBER`

Never propose, create, or assign a `blocked` label, including spelling or case variants. Never use a label or body link as a fallback for a failed native blocking relationship.

### 5. Verify and report

Verify every created issue, label, and native relationship. Return the issue URLs and relationship status. If publication is partial, list what succeeded, what failed, and what remains; report the exact failure without destructive retries or semantic fallbacks.
