---
name: to-spec
description: Turn the current conversation into a specification and publish it to the project's issue tracker.
disable-model-invocation: true
---

Synthesize the current conversation and codebase understanding into a spec. Reuse settled requirements, implementation choices, and testing decisions; do not reopen them for confirmation. Treat proposals and rejected approaches as context unless the user adopted them.

Resolve routine uncertainty from repository evidence. Surface unresolved facts or decisions when they materially affect behavior, scope, contracts, or acceptance criteria. Ask a focused question only when the missing answer prevents an accurate spec; otherwise record the open decision and what it blocks. Complete the rest of the draft while waiting. Do not reopen the interview or invent a decision to make the spec appear complete.

Resolve the publication target from explicit user context, existing repository conventions, or the Git remote. If the target remains ambiguous, ask before publishing. Use the repository's existing triage label vocabulary; do not create or rename labels implicitly.

## Process

1. Reuse relevant repository findings already established in the conversation. Inspect additional code only where needed to ground the spec or resolve a material unknown. Use the project's domain glossary vocabulary throughout the spec, and respect applicable ADRs and the user's latest decisions.

2. Reuse settled testing decisions. Where verification still needs definition, choose existing interfaces or user journeys that can demonstrate the required behavior and catch realistic regressions. Let the behavior determine the number and level of verification surfaces; do not force everything through one seam or the highest possible layer. Mark any new seam as a proposal unless already agreed. Seek a decision only when the choice would materially change scope or a contract; ordinary test mechanics can remain implementation choices.

3. Write the spec using the relevant sections below, then publish it to the resolved project issue tracker. Preserve material open questions explicitly rather than presenting them as settled requirements, and assess readiness before applying labels.

## Readiness

Apply `ready-for-agent` or a documented equivalent only when the label exists, its repository meaning is established, and all of the following hold:

- The spec calls for concrete implementation work, rather than research, discussion, or human coordination as its outcome.
- Required behavior, material constraints, and observable acceptance criteria are settled enough to begin.
- Execution does not depend on an unresolved human decision, approval, access provisioning, or manual action.

Ordinary codebase exploration, reversible engineering choices, and test mechanics do not make a spec unready. Record verified implementation dependencies separately from readiness; a fully specified change may be ready while another issue blocks its start.

If the work is not ready, omit the readiness label and state the missing decision or prerequisite. If the work is ready but no unambiguous readiness label exists, publish without it and report the unavailable label.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Acceptance Criteria

Write non-duplicated, independently verifiable outcomes that together cover the agreed scope. State the observable behavior and the conditions needed to check it, including material failure or recovery behavior established by the requirements.

Use as many criteria as the behavior requires. Do not inflate the list with restated goals, implementation steps, generic “tests pass” statements, or invented scenarios.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

Record settled verification decisions and distinguish any remaining recommendations from requirements. Include only what helps verify this feature:

- The behavior and realistic regressions the checks must distinguish
- The existing interfaces or user journeys those checks exercise
- Relevant prior art in the codebase

Preserve verification through the actual user or consumer path when a lower-level check could bypass the promised behavior. Omit general testing advice and leave reversible test mechanics to implementation.

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

State readiness and any material unresolved decisions or prerequisites, including what each gap blocks. Include other notes only when they affect implementation or verification.

</spec-template>
