---
name: bug-fix-planner
description: Plan a concrete fix for a specific bug, regression, crash, failing test, error, or broken behavior without changing code. Use when the user wants a path forward from a bug report, GitHub issue, stack trace, logs, screenshots, repro steps, or failing test. Do not use for new features, broad refactors, general debugging advice, or requests to directly implement the fix.
---

# Bug Fix Planner

Create a clear, evidence-based plan for fixing a specific bug or defect.

**Plan only. Do not edit files, apply patches, create commits, or implement the fix unless the user explicitly asks for implementation.**

The plan should be specific enough that another engineer could implement it without needing the original conversation.

## Core Behavior

When invoked:

1. Understand the reported bug, affected behavior, expected behavior, and impact.
2. Inspect all available evidence before proposing a fix:
   - user description
   - issue text
   - logs
   - stack traces
   - screenshots
   - failing tests
   - repro steps
   - referenced files
   - relevant source code
3. Trace the likely failing path through the actual code when repository access is available.
4. Distinguish confirmed facts from hypotheses.
5. Recommend one primary fix path, not a loose list of possibilities.
6. Keep the scope limited to resolving the bug.
7. Include validation steps that would prove the bug is fixed and prevent regression.

Ask clarifying questions only when the missing information prevents a useful plan. Otherwise, make the best reasonable assumption, label it clearly, and continue.

## Source and Tool Use

Use available tools to inspect the real issue and code. Do not plan against imagined implementation details.

If a GitHub issue is referenced and a GitHub tool or `gh` CLI is available, inspect the issue and comments.

For example:

```bash
gh issue view <number-or-url> --comments
```

If a repository, file, log, or test is referenced, inspect the relevant artifacts before producing the plan.

If code or issue access is unavailable, say so explicitly and produce a plan based only on the provided evidence. In that case, make reproduction and code inspection early implementation steps.

## Evidence Standard

Classify important claims using one of these labels:

- **Confirmed** — directly supported by code, logs, failing tests, issue text, or repro steps.
- **Likely** — strongly suggested by available evidence but not fully proven.
- **Unknown** — not yet supported; must be verified during implementation.

Do not present a hypothesis as the root cause unless the evidence supports it. If the root cause is uncertain, explain how to confirm or falsify the leading hypothesis.

## Investigation Checklist

Before planning, try to answer:

- What exactly is broken?
- What behavior was expected?
- When or where does the bug occur?
- Is this a regression?
- Can it be reproduced?
- Is there a failing test?
- What code path handles the broken behavior?
- What changed recently, if known?
- What is the smallest change that would fix the root cause?
- What tests or manual checks would catch this in the future?

Do not include this checklist verbatim unless it helps the final answer.

## Plan Structure

Scale the depth to the bug. A simple bug may only need a few sections; a subtle production regression may need all of them. Omit sections that do not apply.

Use this structure:

```markdown
# Bug Fix Plan: <short title>

## Goal

Define what “fixed” means in one or two sentences.

## Current Understanding

Summarize the bug, impact, affected area, and relevant evidence.

Include files, functions, tests, logs, errors, or issue references when known.

## Reproduction

Describe the exact repro steps or failing test.

If reproduction is not yet established, explain how to establish it first.

## Root Cause

State the confirmed root cause.

If not confirmed, state the leading hypothesis, why it is likely, and how to verify it.

## Proposed Fix

Recommend the primary fix.

Include:
- files or functions to change
- what should change
- why this addresses the root cause
- why this is preferable to broader alternatives

## Implementation Steps

Provide ordered, concrete steps.

Each step should be actionable by an engineer.

## Validation

List tests and checks to run.

Include:
- existing tests to run
- new or updated regression tests
- manual verification steps
- edge cases to cover

## Risks and Rollback

Describe likely risks, compatibility concerns, blast radius, and how to revert safely.

## Acceptance Criteria

Provide a short checklist proving the bug is fixed.
```

## Choosing the Fix

Prefer fixes in this order:

1. Correctness
2. Minimal scope
3. Low risk
4. Consistency with existing code patterns
5. Maintainability

Recommend the smallest change that fixes the root cause. Do not recommend a redesign unless a smaller fix would leave the actual defect unresolved.

## Handling Uncertainty

When information is incomplete:

- Do not block on clarification unless necessary.
- State assumptions clearly.
- Identify what must be verified.
- Put verification early in the implementation steps.
- Avoid overclaiming.

Example wording:

```markdown
Root cause is not confirmed yet. The leading hypothesis is that ...
This should be verified by ...
If that hypothesis is wrong, the next most likely area to inspect is ...
```

## Anti-Patterns

Avoid:

- modifying code during planning
- inventing files, functions, or architecture
- listing vague options without choosing a recommendation
- giving generic debugging advice unrelated to the bug
- expanding into unrelated refactors
- treating unverified guesses as facts
- skipping reproduction
- skipping validation
- proposing a workaround when the root cause can be fixed directly
- producing a plan that requires reading the original conversation to understand

## Output Requirements

Write in Markdown with clear headings.

Be concise but concrete. Prefer actionable density over length.

The final plan must include:

- the recommended fix path
- the evidence behind it
- implementation steps
- validation steps
- acceptance criteria

When repo access or reproduction is unavailable, the plan must say so and include the exact next steps needed to close that gap.
