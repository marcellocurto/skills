---
name: blast-radius-audit
description: Find downstream breakage a code change could cause beyond the files it directly touches.
---

# Blast Radius Audit

Find how a change could break behavior outside the edited files. Identify the facts that must be true for the change to be safe and check them against code, documentation, or execution.

Audit only. Do not edit repository files, add permanent tests, apply fixes, commit, publish, or change production or external systems unless separately authorized. Read-only inspection and reversible local diagnostics are allowed. Keep temporary probes outside the working tree and remove them when finished.

## Identify the change

Resolve the pull request, branch, commit, diff, or working changes named by the user. Record exact commits when available. Ask only when the target remains unclear and choosing incorrectly would change the audit.

Read the complete diff and commits, added or removed symbols, relevant tests, callers, and repository instructions. Identify what behavior changes, including effects not obvious from the edited lines. Follow dependencies beyond direct callers when the change could affect them.

## Look for downstream effects

Investigate only paths the change could affect:

- **Data:** stored records, database columns, serialized values, events, cache keys, exports, and consumers in other languages or repositories.
- **Timing:** startup, cleanup, retries, ordering, concurrency, transactions, partial failures, and work that runs later or more than once.
- **Runtime selection:** configuration, environment variables, feature flags, dependency injection, plugins, reflection, generated code, and dynamically loaded paths.
- **Dependency behavior:** the installed library or runtime version, local patches, platform differences, and what the called code actually does.
- **Deployment and recovery:** rollout order, compatibility with older versions, how failures would be detected, and how to recover or roll back.

Verify versions, schemas, and documentation when a conclusion depends on them. Finding no references in a code search does not prove that a function or format is unused; configuration, generated code, or external systems may select or consume it.

## Check the facts that safety depends on

For each possible failure, state what must be true to prevent it. Keep unrelated failures separate. Do not list hypothetical concerns without a plausible path from the change to an affected caller or system.

Describe what you checked and what it establishes: exact code or documentation, a traced path that rules out the failure, an executed test or command, or an observed application workflow. Distinguish these observations from assumptions. Code or a documented contract may be enough; do not run a test merely to repeat proof already obtained.

Prefer existing tests and commands. A temporary probe must use the application's actual code and dependency version, exercise the behavior in question, and fail clearly if the safety assumption is false. Testing a mock or substitute path does not prove the shipped path works.

If a necessary fact cannot be checked, state what is missing and how it could be established. Do not describe an assumption as verified.

## Classify each risk

Use one status per investigated risk:

- **Confirmed:** code, documentation, or execution establishes a failure under conditions that can occur. State those conditions and whether the failure was reproduced or established by inspection.
- **Unresolved:** there is a plausible failure path, but a specific missing fact prevents confirming or ruling it out. Name that fact and the check needed.
- **Ruled out:** the suspected failure cannot occur in the audited scenario, with supporting evidence.

For confirmed or unresolved risks, explain the affected behavior, cause, impact, and evidence about how likely the conditions are. Include detection, recovery, and rollback when they affect the recommendation. Name the simplest check that would resolve any remaining uncertainty.

Mention ruled-out risks only when they explain the verdict or answer a likely concern. Keep them separate from open problems. Do not add minor or hypothetical risks to fill a report.

## Report

Choose the overall verdict in this order:

1. **Material risk found:** at least one confirmed failure would affect correctness, data, compatibility, or operation enough to require attention. Report any unresolved risks alongside it.
2. **Unverified:** no confirmed failure determines the verdict, but an unresolved risk or unchecked safety requirement could change it.
3. **Contained:** the relevant safety requirements have been checked and no material risk remains. State the scope covered; this is not a guarantee about uninspected parts of the system.

Lead with the verdict and use only the detail needed to support it:

- what behavior changes beyond the edited files
- confirmed or unresolved risks, with their evidence and next checks
- facts checked that explain why a likely concern was ruled out
- any verification needed before merge

Stop when each safety requirement has been checked or identified as unverified, each investigated risk has a status, and the report explains any remaining work.
