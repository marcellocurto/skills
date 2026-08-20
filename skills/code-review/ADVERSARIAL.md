# Adversarial Review Mode

Use this mode for requests to interrogate code changes, run a multi-agent or adversarial review, find blind spots, or tear an implementation apart. It supplements the ordinary **Correctness** and **Maintainability** axes; it does not replace them.

## State the Intent

Write one compact paragraph describing what the change is meant to accomplish. Derive it, in order, from the user's latest decisions, the originating issue or specification, the pull-request description, commit messages, and finally the code. Distinguish sourced intent from inference. Ask only when unresolved intent would materially change the review.

Reviewers challenge whether the execution achieves that intent well. If the user also wants the intent itself challenged, use `relentless-review` for that separate question rather than silently changing the review target.

## Prepare One Common Brief

Give every reviewer the same:

- intent paragraph
- fixed point, diff command, and commit list
- applicable repository instructions and documented constraints
- relevant specification and surrounding code paths
- review criteria below

Do not assign personas or different lenses. Independent reviewers should inspect whichever criteria materially apply:

- correctness, error handling, reachable edge cases, state transitions, idempotency, concurrency, and partial failure
- root cause versus symptom suppression
- security paths that can be traced from realistic input to a sensitive operation
- structural fit, ownership, coupling, data-model fit, and compatibility
- behavior-focused verification gaps
- accidental complexity or maintainability costs introduced by the change

Require concrete locations, a reachable failure or maintenance mechanism, and supporting evidence. A preference, hypothetical input with no caller, tooling-enforced style issue, or unrelated pre-existing problem is not a finding. “No findings” is a valid result.

## Run Independent Reviewers

Use two or three read-only sub-agents in parallel, proportionate to the change and available capacity. They inherit the parent model unless the environment provides configured alternatives or the user requests particular models. Do not claim model diversity unless different models were actually used.

Each reviewer returns only:

- severity and concise title
- confidence
- exact location
- concrete finding and evidence
- current-change impact
- smallest credible fix when one is clear

The reviewers do not edit code or apply fixes.

## Apply Lead Judgment

The lead agent has the full conversation and repository context. It must verify findings rather than count votes:

1. Trace each claimed failure or cost against the actual code and constraints.
2. Deduplicate findings that describe the same mechanism.
3. Record agreement and disagreement. Agreement raises investigation priority; it is not proof.
4. Categorize each reviewed finding using the main review contract:
   - **Must fix in current change:** a verified defect that prevents approval
   - **Follow-up:** valid work outside the current change
   - **Suggestion:** an optional improvement
   - **Dismissed:** unsupported, unreachable, preference-only, already handled, out of scope, or contradicted by fuller context

Do not inflate minor observations to fill the report. A classification recommends a disposition; it does not authorize implementation.

## Output

Add an `## Adversarial` section after the two axes with only the useful subsections:

- **Intent**
- **Must fix in current change**
- **Follow-up**
- **Suggestions**
- **Dismissed**
- **Agreement map**

For every retained finding, cite the code and state which reviewers raised it. Explain dismissed findings briefly when they were plausible enough that the user may want to override the lead judgment. If nothing survives validation, say that the adversarial pass found no actionable issue.
