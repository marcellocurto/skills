---
name: to-tickets
description: Turn a plan, spec, issue, or conversation into an approved set of actionable GitHub tickets, then publish them with `gh`, the `ready-for-agent` label, and native parent and blocking relationships. Use when implementation work needs to be broken into dependency-aware GitHub issues or a tracking issue with sub-issues.
---

# To Tickets

Turn existing context into focused GitHub tickets that can be implemented and verified independently.

## Principles

- Use facts from the user, source material, and repository. Do not invent requirements, goals, metadata, relationships, or priority.
- Preserve requirements, constraints, decisions, rationale, meaningful edge cases, and verified findings from prior research. Do not compress away technical detail that would force the implementation agent to repeat exploration.
- Keep cohesive work together. Do not split a useful ticket merely to make it smaller.
- Split only when a ticket has become too broad to implement or review coherently, contains outcomes that can deliver value independently, or needs safety-driven sequencing. When splitting feature work, prefer end-to-end slices that include every layer needed for the behavior without inventing work.
- Declare only genuine blocking dependencies. Sequence or preference alone is not a blocker.
- Do not modify or close a source or parent issue unless the user explicitly asks.
- Avoid generic file inventories and speculative code paths. Include confirmed code locations as current starting points when they save meaningful exploration, but do not present them as authoritative scope.

## Process

### 1. Gather context

Work from the conversation and any referenced plan, spec, issue, comments, repository documentation, ADRs, domain glossary, or prior research. Inspect the codebase only as needed to make the tickets accurate. Ask only when unresolved ambiguity would materially change the ticket set, semantics, or dependency graph.

Resolve the target repository before any GitHub read or write. Search for duplicates only when the user asks or when a likely duplicate would materially affect publication.

### 2. Draft the ticket set

Give each ticket:

- a simple, specific title that explains the outcome in plain language and makes sense without the surrounding plan; avoid terse shorthand, clever wording, and unnecessary jargon
- a body that begins with `## Summary` and a short plain-language explanation of what the ticket is about and why it matters
- a `## Goals` section with clear ordinary bullets describing the outcomes, constraints, and completion signals an implementation agent should follow; never use task-list checkboxes
- a `## Research and findings` section when prior exploration exists, retaining verified findings, relevant evidence, decisions, rejected approaches, pitfalls, and useful technical detail so implementation does not repeat that work; distinguish confirmed facts from hypotheses
- its proposed parent and blockers, when any

Default to substantial tickets with enough scope and context to be useful. Split only when the resulting tickets are easier to execute, verify, or sequence—not to meet an arbitrary size target. Allow enabling work, investigations, migrations, infrastructure, and mechanical refactors when those are the honest units of work. Add a tracking issue only when it provides useful shared context or the user requests one.

For a wide mechanical refactor that cannot land safely in one change, prefer expand–migrate–contract: introduce the new form beside the old, migrate callers in independently safe batches, then remove the old form after the migrations finish. Do not assume a special branching strategy.

Present the exact drafts, proposed native relationships, and labels. Apply `ready-for-agent` to actionable implementation tickets unless the user opts out; do not apply it to tracking-only issues.

Wait for explicit approval before creating anything. Approval of the drafts includes approval for their listed labels and native relationships.

### 3. Publish

Preflight `gh`, authentication, the repository, and the existing `ready-for-agent` label. If the label is missing, report it and ask before creating it; do not silently substitute another label.

Create approved blockers before their dependents, then:

- create each approved issue
- apply `ready-for-agent` to actionable tickets
- create approved parent/sub-issue relationships with GitHub's native relationship
- create approved blocked-by/blocking relationships with GitHub's native relationship

Never propose, create, or assign a `blocked` label, including spelling or case variants. Never use a label or body link as a fallback for a failed native blocking relationship.

### 4. Verify and report

Verify every created issue, label, and native relationship. Return the issue URLs and relationship status. If publication is partial, list what succeeded, what failed, and what remains; report the exact failure without destructive retries or semantic fallbacks.
