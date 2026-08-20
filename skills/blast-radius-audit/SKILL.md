---
name: blast-radius-audit
description: Audit a proposed or completed code change for downstream breakage that direct diff inspection and symbol search may miss. Use for "what could this break?", blast-radius analysis, risky small diffs, dependency upgrades, or changes to shared schemas, serialization, persistence, lifecycle timing, or cross-service contracts. Read-only; not a standards, specification, or general code-quality review.
---

# Blast Radius Audit

Find concrete ways a change could break behavior outside its visible diff, then establish the smallest set of facts its safety depends on.

Audit only. Do not edit repository files, add permanent tests, apply fixes, commit, publish, or mutate production or external systems unless the user separately authorizes those actions. Read-only inspection and reversible local diagnostics are allowed. Put any throwaway probe outside the working tree and remove it when finished.

## Establish the Change

Resolve the exact change under review from the user's named pull request, branch, commit, diff, or working changes. Record the fixed point when one exists. Ask only when choosing the wrong target would materially change the audit.

Inspect:

- the complete diff and commits
- added, changed, and deleted symbols
- the behavior that changes, including semantic effects not obvious from the edited lines
- relevant tests, callers, and repository instructions

Direct callers are the starting point, not the blast-radius result.

## Trace Hidden Edges

Follow only the edges that the change makes plausible:

- **Data:** persisted records, database columns, serialized JSON, wire formats, events, cache keys, exported files, and consumers in other languages or repositories
- **Time:** initialization, teardown, retries, ordering, concurrency, transactions, partial failure, and work that runs later or more than once
- **Runtime selection:** configuration, environment variables, feature flags, dependency injection, plugins, reflection, generated code, and dynamically loaded paths
- **Dependency semantics:** the exact pinned library or runtime version, local patches, platform differences, and behavior behind the called function rather than its name
- **Operational contracts:** rollout order, backward compatibility, mixed-version operation, detectability, recovery, and rollback

Verify the exact version, schema, contract, or external source whenever a conclusion materially depends on it. A search that finds no caller is evidence about the searched symbol graph, not proof that no implicit consumer exists.

## Establish the Safety Claims

Identify the smallest set of load-bearing facts that must hold for the change to be safe. Do not force unrelated risks into one claim, and do not produce a long inventory of hypothetical concerns.

For each claim, obtain the strongest proportionate evidence that is safely available:

1. **Inferred:** reasoned from the change but not independently established
2. **Source-backed:** supported by exact application, dependency, schema, or contract locations
3. **Failure path excluded:** the suspected bad case was traced end to end and cannot reach an observable failure
4. **Executed:** an existing test, focused command, or temporary probe exercised the real shipped path and would fail if the claim were false
5. **Journey-proven:** reproduced through the real application, integration, or consumer workflow

Prefer existing tests and commands. A temporary probe must import the same code and dependency version the application ships, exercise the behavior in question rather than a mock of it, and fail loudly when the claim is false. Do not use a substitute path to overstate certainty.

Mark a claim `unverified` when the available evidence does not establish it. State the exact missing proof; do not round an inference up to safety.

## Judge Material Risk

Keep a risk only when there is a concrete failure mechanism and affected consumer. For each material risk, state:

- where and how the failure reaches observable behavior
- likelihood, supported by evidence rather than an adjective
- impact, detectability, recovery, and rollback when relevant
- whether it is `confirmed`, `credible`, `cleared`, or `unverified`
- the cheapest decisive check

List cleared risks separately so the user can see what was investigated without mistaking them for open problems. Do not pad the audit with generic possibilities.

## Output

Lead with a verdict: `contained`, `material risk found`, or `unverified`.

Include only the sections that add evidence:

- **Behavioral change:** what changes beyond the literal diff
- **Safety claims:** each claim, evidence level, proof, and status
- **Material risks:** concrete open or confirmed failure mechanisms
- **Cleared:** plausible risks checked and ruled out
- **Before merge:** the cheapest remaining test, probe, or real-world check

If no material risk remains, say so directly while preserving any evidence limits. Stop when every load-bearing safety claim is either established or explicitly unverified and every material risk has a status.
