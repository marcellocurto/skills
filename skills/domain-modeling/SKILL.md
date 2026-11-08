---
name: domain-modeling
description: Define and maintain the codebase's shared domain terms and architectural decisions. Use when a domain term is unclear or disputed, when a lasting architectural decision is made or stops holding, when the user asks to update or clean up the glossary or decision records, or when another skill runs it.
---

# Domain Modeling

Clarify the project's domain concepts and the decisions that shape them. Use this skill when defining or revising those meanings; merely reading an existing glossary does not require a modeling session.

## Choose the working mode

- **Discussion or proposed edits:** For discussion, review, or read-only requests, keep definitions, decisions, and proposed document changes in the conversation. Do not create or edit files.
- **Documentation updates:** When the user asks to create or maintain domain documentation, or requests a workflow that includes recording it, write settled terms and qualifying decisions within that scope. Honor authorization already given without asking again for each entry. If writes are limited to particular documents, keep other proposed records in the conversation.

Loading this skill alone does not authorize documentation writes. When the request does not establish write intent, continue in discussion mode. Recording a model does not authorize implementing it or renaming code.

## Find the existing documentation

Inspect repository guidance and relevant documentation for the current glossary, context map, ADR location, and document formats. Follow existing names, links, context ownership, and numbering before creating anything. For ADRs, a convention the project documents in its instructions, an ADR README, or an ADR template overrides [ADR-FORMAT.md](./ADR-FORMAT.md) and this skill's rules for revising and deleting ADRs. The style of existing records is not such a convention. A glossary or ADR directory with a different name is not missing documentation.

If no convention exists, use `CONTEXT.md` for domain terms and `docs/adr/` for architectural decisions. Create them only in documentation-update mode when there is agreed content to record. Use an existing context map, whatever its filename, to locate domain-specific records; do not infer that the whole project has one context merely because a root `CONTEXT.md` exists.

## During the session

### Challenge against the glossary

Compare the intended meaning with the glossary. Ask about a conflict when it changes a domain distinction, behavior, ownership, or contract. Ordinary synonyms or wording variations that clearly refer to the same concept do not need an interruption; use the established term in your response.

### Sharpen fuzzy language

Use context and available evidence to interpret an overloaded term. If materially different meanings remain plausible, explain the distinction and ask a focused question. Recommend a canonical term when useful, but do not treat that recommendation as an agreed change or police wording for consistency alone.

### Discuss concrete scenarios

Use concrete scenarios when they distinguish plausible meanings or expose an unresolved domain rule. Focus on cases that could change the current decision; do not generate edge cases merely to prolong the discussion.

### Cross-reference with code

Check relevant code when it can establish current behavior or clarify a material distinction. Keep implemented behavior separate from the user's intended model. If they differ, establish whether the user is describing a planned change, correcting stale documentation, or resolving an inconsistency; do not reopen an explicit decision merely because the code has not caught up.

### Record settled meanings

In documentation-update mode, record a resolved term in the existing glossary as its meaning settles. In discussion mode, retain the agreed definition or proposed text in the response. Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) only when the project has no established format.

Keep glossary entries focused on domain meaning. Put implementation decisions in the appropriate architectural record rather than a definition. Preserve unrelated sections of existing documents; do not reshape a multipurpose `CONTEXT.md` into a glossary-only file. Keep unresolved proposals and assumptions distinct from agreed content.

### Record only qualifying decisions as ADRs

A decision qualifies for an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off or an outside constraint**: there were genuine alternatives and you picked one for specific reasons, or a constraint invisible in the code ruled the obvious option out

If any of the three is missing, do not create or propose an ADR. When documentation updates are already authorized, record qualifying settled decisions without requesting approval again. Otherwise propose the record in the conversation. Write it as [ADR-FORMAT.md](./ADR-FORMAT.md) describes, which also lists examples of qualifying decisions.

### Keep ADRs true of the current system

When a decision changes or stops holding, rewrite its ADR to state what the system does now, or delete the ADR when nothing that replaces it qualifies. Git history keeps the earlier version. When you delete or merge an ADR, fix the links in other documents that pointed to it. Do not mark an ADR as superseded or deprecated, and do not keep a record of a decision the system no longer follows. When the old approach is worth remembering as a rejected option, state it in a "We rejected" sentence of the current ADR.

## Prune existing ADRs

When the user asks to review, clean up, or simplify the ADRs, check each one against the current code and documentation, then:

1. Rewrite an ADR whose decision was replaced by one that qualifies, so it states the current decision. Delete an ADR whose decision the system no longer follows when nothing that qualifies replaced it, such as a workaround for a constraint that no longer applies or rules for a feature that was removed.
2. Merge ADRs that the grouping rule in [ADR-FORMAT.md](./ADR-FORMAT.md) puts together.
3. Rewrite the rest in the shape [ADR-FORMAT.md](./ADR-FORMAT.md) describes, removing what it says to leave out.

In discussion mode, present the deletions, merges, and rewrites as a proposal instead.

## Finish

Summarize the resolved meanings and decisions, material open questions, and documents updated or proposed. Read back written changes to confirm they express the agreed meaning and preserve existing context. Do not claim proposed text was saved in discussion mode.
