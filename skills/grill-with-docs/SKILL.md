---
name: grill-with-docs
description: Stress-test a plan through questions while recording the resulting domain terms and lasting architectural decisions. Use when the user asks to grill a plan with docs, or to record its terms and decisions while questioning it. For questions alone, use `grilling`.
---

# Grill with Docs

Stress-test the requested plan through conversation and keep agreed domain language and lasting decisions in the project's documentation. This skill runs the `grilling` skill for the questions and the `domain-modeling` skill for the glossary and architectural decision records, and adds only how the two work together.

## Documentation scope

A request to use this workflow asks for settled terms and qualifying decisions to be recorded, so run `domain-modeling` in its documentation-update mode as answers settle. When the user asks for read-only or proposed edits, run it in discussion mode instead. If the user limits writes to particular documents, update only those.

Record only what `domain-modeling` qualifies as a domain term or an architectural decision. Keep routine choices, tentative proposals, and unresolved questions in the conversation, and don't turn them into specifications or tracker issues unless the user asks.

## Question, resolve, record

1. Run a round of `grilling` on the decision the user wants to resolve.
2. Record what the round settled with `domain-modeling`, before asking the questions it unlocks.
3. If an answer revises an earlier decision, update the affected record so the documentation and the discussion agree.

Repeat until `grilling` finishes. Then report the settled conclusions, the remaining material questions, and the documentation changed or proposed.
