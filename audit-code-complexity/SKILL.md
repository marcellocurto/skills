---
name: audit-code-complexity
description: Audit code and tests for accidental complexity, overengineering, poor patterns, and low-value tests. Use for current-state audits of a feature, module, or codebase, or change-scoped audits of a diff, PR, branch, or working changes. Distinguish essential complexity from removable complexity and recommend behavior-preserving simplifications. Read-only unless fixes are explicitly requested.
---

# Audit Code Complexity

Find what is materially harder to understand, change, or verify than the problem requires.

## Scope

Choose from the user's wording:

- **Current-state**: audit the target as it exists, regardless of when complexity was introduced.
- **Change-scoped**: report only complexity introduced or materially worsened by the named changes; inspect surrounding code only for context.

Do not infer change scope merely because a repository has changes. If both modes are requested, report them separately. Ask only when genuine ambiguity would materially change the audit.

## Method

Inspect the target, repository instructions, callers, tests, configuration, and only the requirements or docs needed to understand behavior and constraints.

Look for:

- unjustified indirection, wrappers, genericity, extension points, dependencies, or infrastructure
- tangled control flow, flag combinations, implicit state, invalid states, or multiple sources of truth
- repeated transformations, leaky types, wide APIs, hidden side effects, or unclear ownership
- duplicated policy, scattered edits for one change, or modules with unrelated responsibilities
- misleading names, distant cause and effect, broad mutation, dense expressions, or clever code
- speculative guards, fallbacks, compatibility paths, or dead machinery
- low-value tests and test harness complexity

Useful smell labels include Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Conditionals, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chain, and Middle Man. Treat them as clues, not automatic violations.

Include a finding only when:

1. The code creates a concrete maintenance, comprehension, correctness, or operational cost.
2. The claim is supported by code, usage, tests, or requirements.
3. A simpler alternative is concrete and preserves required behavior and contracts.
4. The benefit outweighs migration and regression risk.

Line count, nesting, complexity metrics, and unfamiliarity are clues—not findings.

## Tests

Ask: **What realistic bug or regression would this catch?**

Flag tests that merely restate configuration, constants, metadata, static content, or private implementation; assert mocks or calls instead of outcomes; duplicate stronger coverage; or add more machinery than the behavior warrants.

Prefer observable behavior. Keep a direct configuration test only when the exact representation is itself a supported consumer, runtime, installer, or serialization contract. Classify test recommendations as **Keep**, **Fix**, or **Cut**.

## Output

Lead with a verdict, then prioritized findings. For each finding include:

- impact and confidence
- exact location and evidence
- concrete cost
- simpler alternative
- behavior or contracts that must remain unchanged

Add justified complexity, simplification order, and validation only when useful. If no material findings exist, say so directly.

## Rules

- Audit only; do not edit unless explicitly asked.
- Prefer local simplification over rewrites.
- Do not create an abstraction solely to remove similar-looking code; require a shared concept.
- Preserve domain distinctions, data semantics, source of truth, identity, routing, validation, security, accessibility, and compatibility.
- Skip formatter, linter, naming, and style nits unless they materially obscure behavior.
- Do not reward coverage for its own sake or demand tests for every line.
- Report bugs, security, or performance issues only when caused or concealed by the complexity under review.
