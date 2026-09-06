# Adversarial Review Mode

Use this mode for requests to interrogate code changes, run a multi-agent or adversarial review, find blind spots, or tear an implementation apart. Apply these criteria within the reviewer budget in [SKILL.md](SKILL.md#budget-the-reviewers). Preserve separate **Correctness** and **Maintainability** judgments; this mode does not require a second group after an ordinary review.

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

Give the primary adversarial reviewers the same criteria rather than different personas. Each should inspect whichever criteria materially apply and keep the two axis judgments separate:

- correctness, error handling, reachable edge cases, state transitions, idempotency, concurrency, and partial failure
- root cause versus symptom suppression
- security paths that can be traced from realistic input to a sensitive operation
- structural fit, ownership, coupling, data-model fit, and compatibility
- behavior-focused verification gaps
- accidental complexity or maintainability costs introduced by the change

Require concrete locations, a reachable failure or maintenance mechanism, and supporting evidence. A preference, hypothetical input with no caller, tooling-enforced style issue, or unrelated pre-existing problem is not a finding. “No findings” is a valid result.

## Run Independent Reviewers

Use the two primary reviewers allocated for the review. If ordinary review has already started, extend their assignments with the missing adversarial coverage and reuse the pinned evidence. An additional reviewer needs a concrete gap or risk and counts against the overall budget; do not launch a fresh two- or three-agent group merely because this guide was loaded.

Reviewers inherit the parent model unless the environment provides configured alternatives or the user requests particular models. Do not claim model diversity unless different models were actually used. Keep reviewers' conclusions out of each other's briefs. For a targeted additional investigation, provide the relevant artifacts and unresolved question without prescribing the expected verdict. If delegation is unavailable, use distinct local passes and disclose the lack of independent agents.

Each primary reviewer returns separate Correctness and Maintainability verdicts, with only the useful evidence gaps and findings for each. A targeted additional reviewer reports the assigned coverage and its findings without claiming to have reviewed both axes completely. Findings include:

- controlling axis, severity, and concise title
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

Include validated findings in the corresponding axis in the main report so its verdict reflects all review evidence. For each retained finding, cite the code and identify which reviewers raised it. Do not repeat the same finding in multiple sections.

Append an `## Adversarial` section only with useful additional context: the intent tested, coverage limits, material agreement or disagreement, or plausible dismissed leads the user may want to reconsider. Reference findings already reported under the axes rather than restating them. If nothing survives validation, say that adversarial review found no actionable issue; do not invent findings to justify the effort.
