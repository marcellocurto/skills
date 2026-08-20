---
name: product-ui-audit
description: Audit an existing product interface and propose a product-native UX direction without editing code. Use for screenshots, live pages, navigation, information density, hierarchy, workflow clarity, and high-scale operational views. Not for implementation or unconstrained visual experimentation.
---

# Product UI Audit

Audit how well an existing interface helps its real user understand, decide, and act.

Audit only. Do not edit code or design files. Use `design-system-ui` for an explicitly requested implementation and `wild-frontend` for explicitly requested unconstrained creative work.

## Goal

Give one coherent, product-aware direction that improves usability and visual quality without replacing required content, inventing product behavior, or defaulting to generic SaaS composition.

## Understand the Product

Inspect the actual screen or screenshot and the minimum relevant product context. When repository or live-page access exists, inspect nearby screens, shared components, tokens, content, and interaction patterns only until the local design language and workflow are clear.

Establish:

- **User**: who uses the interface and how often
- **Job**: the primary decision or action the screen supports
- **Information**: what must be scanned, compared, understood, or trusted
- **Scale**: realistic item counts, content length, and operational extremes
- **States**: loading, empty, error, partial, stale, selected, expanded, disabled, and recovery states that can actually occur
- **Constraints**: required content, business claims, accessibility, platform conventions, and existing product patterns

If key context is unavailable, state which conclusions are provisional. Do not fabricate product requirements from familiar UI patterns.

## Audit the Interface

Prioritize findings that materially affect the job:

- information architecture and workflow
- navigation, orientation, and progress
- scanning, comparison, density, and progressive disclosure
- visual hierarchy, typography, spacing, and composition
- interaction affordances and feedback
- accessibility and responsive behavior
- trust, operational clarity, and recovery

Judge the interface at representative scale, not only the visible fixture. A control that works for ten items may fail for hundreds; a compact label may fail with real localized content.

Separate:

- **Usability defect**: blocks, misleads, hides, or makes the task materially harder
- **Product gap**: information or behavior needed for the job is absent
- **Visual weakness**: composition or hierarchy reduces clarity or quality
- **Preference**: a defensible aesthetic choice, not a defect

## Choose a Direction

Recommend one dominant screen model rather than a collection of unrelated component suggestions. Prefer removal, consolidation, hierarchy, and progressive disclosure before adding new surfaces.

Avoid defaulting to:

- nested cards or boxed regions without a grouping purpose
- repeated status, badges, labels, or calls to action
- loading states for content that is static or immediately available
- ambiguous icons or controls that imply unsupported interaction
- dashboards, summaries, filters, or metrics that do not change a decision
- removing required copy or business content instead of improving its presentation
- generic advice such as “improve spacing” without a concrete compositional change

Preserve the product's domain language and distinguish authoritative facts from estimates, heuristics, or decorative indicators.

## Output

Lead with a direct verdict on the current interface and its largest usability gap.

Then provide, as applicable:

- **User and job**: the operative task model
- **Prioritized findings**: evidence, impact, and why the current design fails
- **Recommended direction**: the coherent screen model and hierarchy
- **Remove or consolidate**: what should disappear or merge
- **Critical states and scale**: conditions the redesign must support
- **Implementation handoff**: concrete behavior and composition guidance without writing code

Use a compact wireframe or flow only when it explains the proposed hierarchy better than prose. Do not pad the audit with generic design principles.

## Stop Rules

Stop when the dominant product problem, coherent direction, material findings, and required states are clear enough for design or implementation. If the current interface is already strong, say so and limit recommendations to genuine gaps.
