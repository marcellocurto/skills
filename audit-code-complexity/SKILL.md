---
name: audit-code-complexity
description: Audit code for accidental complexity, overengineering, and behavior-preserving simplifications. Use for current-state audits of a feature, module, or codebase, or change-scoped audits of a diff, PR, branch, or working changes. Inspect tests only when their harness, setup, or coupling creates or conceals complexity. Use test-quality-audit when tests are the main subject. Read-only unless fixes are explicitly requested.
---

# Audit code complexity

Find what is materially harder to understand, change, or verify than the problem requires.

## Scope

Choose from the user's wording:

- **Current-state.** Audit the target as it exists, regardless of when complexity was introduced.
- **Change-scoped.** Report only complexity introduced or materially worsened by the named changes. Inspect surrounding code only for context.

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
- test harnesses, fixtures, mocks, or setup that make production behavior harder to understand or change

Useful smell labels include Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Conditionals, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chain, and Middle Man. Treat them as clues, not automatic violations.

Include a finding only when:

1. The code creates a concrete maintenance, comprehension, correctness, or operational cost.
2. The claim is supported by code, usage, tests, or requirements.
3. A simpler alternative is concrete and preserves required behavior and contracts.
4. The benefit outweighs migration and regression risk.

Line count, nesting, complexity metrics, and unfamiliarity are clues, not findings.

## Test boundary

Inspect tests when they establish a contract, explain intended behavior, or provide evidence for a complexity finding.

Report test-related complexity only when the test architecture creates or conceals a concrete cost. Examples include shared setup with hidden state, helper layers that obscure behavior, duplicated fixtures that encode policy in several places, test-only seams that force production indirection, or mocks that hide unclear ownership.

Do not turn this into a general review of test value, coverage, snapshots, assertions, or missing cases. When tests are the main subject, use `test-quality-audit` instead.

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
- Do not expand the audit into a standalone test-quality review.
- Report bugs, security, or performance issues only when caused or concealed by the complexity under review.
