---
name: grill-with-docs
description: Stress-test a plan through questions while recording the resulting domain terms and lasting architectural decisions. Use when the user asks to grill a plan with docs, or to record its terms and decisions while questioning it. For questions alone, use `grilling`.
---

# Grill with Docs

Stress-test the requested plan through conversation and keep agreed domain language and lasting decisions in the project's documentation. This skill runs the `grilling` skill for the questions and the `domain-modeling` skill for the glossary and architectural decision records, and adds only how the two work together.

## Documentation scope

A request to use this workflow is a request to record settled terms and qualifying decisions, so run `domain-modeling` in its documentation-update mode unless the user asks otherwise. Permission to record doesn't extend to commits, pushes, or publishing. Don't turn routine choices or open questions into specifications or tracker issues unless the user asks.

## Question, resolve, record

1. Read the existing glossary, context map, and relevant decision records as `domain-modeling` describes, so the questions build on what is already recorded.
2. Run a round of `grilling` on the decision the user wants to resolve.
3. Record what the round settled with `domain-modeling`, before asking the questions it unlocks.
4. If an answer revises an earlier decision, update the affected record so the documentation and the discussion agree.

Repeat from step 2 until `grilling` finishes, then give one report that combines both skills' summaries.
