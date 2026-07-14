---
name: audit-code-complexity
description: Audit existing code and tests for unnecessary complexity, overengineering, poor patterns, awkward control or data flow, unjustified abstractions, inelegant implementations, and low-value tests that restate configuration or implementation instead of protecting behavior. Use for either a current-state audit of a feature, module, or codebase, or a change-scoped audit limited to complexity introduced or worsened by a diff, PR, branch, or working changes. Report findings without editing code unless the user explicitly asks for fixes.
---

# Audit Code Complexity

Identify accidental complexity that can be removed without weakening required behavior, contracts, or safety.

The governing question is: **What is materially harder to understand, change, or verify than the problem requires?**

## Goal

Produce a prioritized, evidence-based audit of actual code. Distinguish essential domain complexity from complexity introduced by the implementation, and recommend the smallest behavior-preserving simplification for each material finding.

## Success Criteria

- Inspect the relevant implementation, callers, tests, and repository conventions before judging it.
- Explain the concrete cost of each finding: cognitive load, change amplification, hidden coupling, invalid states, duplicated policy, brittle control flow, or avoidable operational risk.
- Show that a simpler alternative fits the real requirements and current usage.
- Identify tests that add maintenance cost or false confidence without catching a realistic behavioral regression.
- Preserve public behavior, data semantics, source of truth, identity, routing, security, accessibility, and compatibility unless the user explicitly authorizes a contract change.
- Prioritize material findings and omit generic style advice.
- Say clearly when the code is already appropriately simple.

## Audit Workflow

### 1. Choose the Audit Mode and Target

Use the user's wording to choose one mode:

- **Current-state audit**: evaluate the requested feature, module, file set, tests, or codebase as it exists now, regardless of when the complexity was introduced.
- **Change-scoped audit**: evaluate only the diff, PR, branch, commit range, or working changes the user named. Report complexity caused or materially worsened by those changes. Inspect surrounding code for context, but do not turn pre-existing issues into findings.

Do not default to change-scoped mode merely because the repository has uncommitted changes or history. State the chosen mode and target briefly. If the request is genuinely ambiguous and the modes would produce materially different results, ask; otherwise make the narrowest reasonable assumption and state it.

If the user explicitly asks for both, report current-state findings and change-introduced findings separately; do not mix their scopes.

The user may narrow either mode to a concern such as tests, abstractions, state, or a specific path. Honor that boundary.

### 2. Recover Required Behavior and Constraints

Recover the reason for the code before deciding that its complexity is unnecessary. Read applicable repository instructions and only the requirements, docs, callers, tests, configuration, and local conventions needed to understand the target. Do not ask for context that can be recovered from the repository.

Trace enough of the real path to understand:

- entry points and callers
- inputs, outputs, state, and side effects
- data ownership and source of truth
- error and recovery behavior
- compatibility and performance constraints
- tests and configuration that reveal intended behavior or a supported contract

Do not infer that unfamiliar code is unnecessary. If intent or usage remains uncertain, state the uncertainty and reduce confidence rather than inventing a requirement.

### 3. Look for Accidental Complexity

Audit the dimensions that matter for the target:

- **Indirection and abstraction**: wrappers that only forward, abstractions with one real use, premature extension points, generic machinery without demonstrated variation, or layers that obscure ownership.
- **Control flow and state**: deep nesting, flag combinations, duplicated branches, temporal coupling, split lifecycle logic, implicit transitions, or state that permits invalid combinations.
- **Data flow and modeling**: repeated transformations, parallel representations, boolean blindness, leaky types, primitive obsession, unclear ownership, or multiple sources of truth.
- **APIs and boundaries**: wide interfaces, option bags with coupled fields, hidden side effects, inconsistent contracts, or internal convenience exposed as public surface area.
- **Duplication and reuse**: duplicated policy that can drift, or forced reuse that couples unrelated concepts. Do not treat similar-looking code as the same concept without evidence.
- **Dependencies and frameworks**: libraries, patterns, configuration, caching, concurrency, or infrastructure whose cost exceeds the requirement they serve.
- **Defensive and compatibility code**: speculative fallbacks, unreachable guards, swallowed errors, redundant validation, or legacy paths with no verified consumer. Preserve necessary boundary validation and compatibility.
- **Local implementation quality**: misleading names, distant cause and effect, mutation across broad scopes, dense expressions, comments compensating for opaque code, or cleverness that hides straightforward behavior.
- **Test value and suite complexity**: tests that cannot name a realistic regression, merely restate configuration, constants, metadata, prompt prose, static content, or private implementation, assert calls or mocks instead of outcomes, duplicate stronger coverage, or require more harness machinery than the behavior warrants.

For suspicious tests, ask what behavior they claim to protect, what they actually protect, whether real behavior could break while they still pass, and whether a harmless refactor would break them. Classify the recommendation as **Keep**, **Fix**, or **Cut**.

Configuration can itself be behavior when a consumer, installer, runtime, or published format depends on its exact shape. Keep a direct configuration or contract test when that exact representation is supported behavior. Otherwise prefer a test of the observable effect over a test that copies production literals into assertions.

Treat line count, function length, nesting depth, and complexity metrics as investigation clues, not findings by themselves.

Use named smells as labels for judgment calls when they make a finding clearer:

- **Mysterious Name**: a name hides what the value or operation means.
- **Duplicated Code**: the same policy or logic can drift in multiple places.
- **Feature Envy**: behavior depends more on another module's data than its own.
- **Data Clumps / Primitive Obsession**: recurring loose values represent one domain concept.
- **Repeated Conditionals**: the same decision is spread across multiple branches or sites.
- **Shotgun Surgery**: one conceptual change requires scattered edits.
- **Divergent Change**: one module changes for unrelated reasons.
- **Speculative Generality**: extension points or abstractions serve no current requirement.
- **Message Chain / Middle Man**: navigation or delegation adds coupling without useful policy.
- **Refused Abstraction**: an implementation inherits or conforms to machinery it mostly bypasses.

Label these as possible smells, not automatic violations. Recommend the usual refactoring only when it fits the repository, preserves the domain model, and is simpler in this specific code.

### 4. Prove Each Finding

Include a finding only when all of these are true:

1. The current design imposes a concrete cost.
2. The evidence is visible in the code, usage, tests, or requirements.
3. A more direct alternative can be described concretely.
4. The alternative preserves required behavior and important contracts.
5. The simplification benefit outweighs migration and regression risk.

For every finding, identify:

- the exact location and relevant call path
- what makes the complexity unnecessary or the pattern harmful
- the simpler shape
- what must remain unchanged
- impact and confidence

If the alternative merely moves complexity elsewhere, shortens code without clarifying it, or depends on speculative future cleanup, do not recommend it.

For a test finding, name the realistic bug the test should catch, explain why the current test would miss it or fail for the wrong reason, and recommend the smallest stronger behavioral assertion or removal when no valuable behavior exists.

### 5. Prioritize by Payoff

Use these impact levels:

- **High**: materially increases correctness risk, change amplification, hidden coupling, or operational failure across an important path.
- **Medium**: creates recurring maintenance or comprehension cost in an actively used path.
- **Low**: causes localized friction with a safe, obvious cleanup. Omit low-impact findings unless they are unusually clear or the user requests exhaustive coverage.

Order findings by impact, then confidence. Keep separate problems separate, but combine repeated instances with one root cause.

## Output

Lead with the verdict and findings. Use only sections that add value.

- **Verdict**: whether the implementation is appropriately simple, mildly overbuilt, materially overcomplicated, or structurally difficult to maintain.
- **Findings**: prioritized findings with impact, confidence, file/line evidence, concrete cost, simpler alternative, preservation constraints, and **Keep/Fix/Cut** when the finding concerns tests.
- **What should stay**: complexity that is justified by the domain or operational requirements and should not be flattened.
- **Simplification sequence**: the smallest safe order of work when findings depend on one another.
- **Validation**: tests, checks, or observations that would prove behavior was preserved.

If no material findings exist, say so directly. Mention remaining uncertainty or review gaps instead of manufacturing criticism.

## Constraints

- Audit only. Do not edit files unless the user explicitly requests implementation.
- Critique the code, not its authors.
- Prefer local simplifications over rewrites when they achieve the same result.
- Do not recommend an abstraction solely to remove duplication; require a shared concept and a stable boundary.
- Do not collapse domain distinctions, ownership boundaries, validation, or explicit state merely to reduce lines.
- Do not substitute personal taste for repository conventions or evidence.
- Do not report formatter, naming, or style nits unless they materially obscure behavior.
- Do not reward coverage for its own sake or require tests for every helper, branch, configuration value, or line.
- Do not expand into a general bug, security, or performance audit. Report those issues only when they are caused or concealed by the complexity under review.

## Stop Rules

Stop when the material accidental complexity, justified complexity, safest simplification order, and preservation checks are clear. Ask only when missing context would materially change a finding or authorize a contract change.
