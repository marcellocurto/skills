---
name: design-system-ui
description: Build polished production UI that extends a product's existing design system and patterns.
disable-model-invocation: true
---

# Design System UI

Create production-grade frontend UI that feels native to the product and sharper than a default implementation.

For multi-step work, start with a short user-visible update that names the product context you are inspecting first.

## Goal

Use the existing product as the creative material. The result should feel native to the app, visually intentional, consistent with usable components and tokens, and improved through hierarchy, composition, interaction quality, and polish.

## Success Criteria

- The UI works as real code in the requested or existing stack.
- Existing components, tokens, typography, layout conventions, icon sets, and accessibility patterns are reused when they fit.
- The design has a clear product-aware direction instead of generic SaaS defaults.
- The composition is deliberate at both page and detail scale: hierarchy, alignment, proximity, rhythm, and negative space guide attention without accidental gaps or visual drift.
- States the task can actually reach are handled, such as loading, empty, error, disabled, selected, focused, hovered, active, success, destructive, long content, and small screens. States are not invented merely for completeness.
- Responsive behavior is checked for common viewport sizes.
- The actual route is rendered with representative data volume and content length, then compared with adjacent product screens when the environment allows it.
- Every new surface, loader, icon, badge, card, and state communicates something necessary for the user's task.

## Context Budget

Before coding, inspect only the context needed to make the UI fit:

- nearby pages with a similar purpose
- shared components and page shells
- tokens, theme files, Tailwind/CSS config, and typography
- spacing, radius, borders, shadows, surfaces, icons, and motion
- existing loading, empty, error, disabled, focus, and responsive patterns

Stop discovery once the product context, reusable primitives, styling system, and validation path are clear enough to implement. Continue only when a missing pattern would materially affect correctness, visual fit, or accessibility.

## Product Direction

Before implementing, choose a concise direction:

- **Purpose**: what job the interface does
- **User**: who uses it and what they are deciding or accomplishing
- **System language**: what the existing UI already communicates
- **Upgrade move**: what can be made more distinctive while still fitting
- **Signature detail**: the one detail that makes the result feel considered

Use [references/design-moves.md](references/design-moves.md) only when you need more examples for typography, layout, color, surface, motion, or states.

## Craft Standard

Work as a visual craftsperson. The design system supplies a vocabulary, not a finished composition; applying the right tokens is not a substitute for judgment.

- Compose the whole page before polishing isolated components. Establish the focal point, reading order, dominant alignments, grouping, balance, and transitions between regions.
- Treat space as active material. Outer margins, section gaps, internal padding, line spacing, and empty areas should create hierarchy and rhythm. Avoid leftover gaps, double padding, cramped edges, and mechanically uniform spacing where relationships differ.
- Apply enduring graphic-design principles deliberately: hierarchy, alignment, proximity, repetition, contrast, scale, balance, rhythm, and figure-ground. Use them to clarify the product rather than as a checklist or stylistic overlay.
- Tune visible relationships, not only numeric values. Check baselines, icon-and-label pairs, text blocks, control heights, border junctions, optical centering, line length, wrapping, and the way neighboring surfaces share an edge.
- Review at both scales: zoom out for composition, density, and whitespace; zoom in for the small inconsistencies that make an interface feel unresolved. Continue refining until every prominent placement looks intentional.

## Constraints

- Write real working frontend code that follows project conventions.
- Treat user-supplied copy, business claims, interaction meaning, screenshots, and existing information architecture as product constraints unless the user asks to reconsider them. Do not solve a presentation problem by deleting required content, weakening claims, or changing product semantics.
- Keep changes within the requested screens and components. Change a shared primitive only when it is the demonstrated cause or the requested result genuinely requires it, then verify the affected consumers.
- Prefer existing primitives, tokens, icon sets, animation utilities, accessible HTML, keyboard-friendly interactions, responsive behavior, clear component structure, and scoped styling.
- Add new visual primitives only when they improve the design and could fit naturally into the product system.
- Do not introduce asynchronous behavior, loading states, or layout shifts for static or synchronous content.
- Avoid arbitrary custom styles, decoration without product purpose, extra components when existing primitives fit, centered-card layouts by default, turning every content group into a bordered card, false interaction affordances, timid evenly distributed color, and purple-gradient polish pasted onto unrelated products.

## When There Is No Clear Design System

Create a small local design direction: compact color system, type hierarchy, spacing rhythm, radius and shadow rules, button/input/card treatment, responsive layout, and interaction states.

Make it coherent through a few strong choices rather than many unrelated effects.

## Final Verification

Before finalizing, inspect the implementation through the real application route and interaction when accessible:

- Use representative data volume, realistic localized copy, long values, and the scale conditions that could change the layout or interaction model.
- Check the relevant viewport sizes and every reachable state introduced or affected by the work.
- Compare the result with adjacent product screens for hierarchy, density, typography, spacing, surfaces, control treatment, and interaction language.
- Inspect the page as a single composition and at detail scale. Check focal order, alignment lines, section rhythm, negative space, nested padding, text wrapping, baselines, optical balance, and responsive redistribution of space.
- Review every new surface, loader, icon, badge, card, and state. Keep it only when it communicates necessary grouping, status, action, or feedback better than the simpler composition.
- Confirm static or immediately available content does not gain unnecessary loading UI, asynchronous behavior, empty placeholders, or layout shifts.

Run applicable code validation as well, but do not treat a build, typecheck, or component-level test as proof of visual quality. If the real route cannot be inspected, report the gap and the next best verification instead of claiming the UI is fully verified.

## Output

When implementing, provide scoped code that is ready to run in the user's stack. In the final response, lead with the completed result, then name the product-aware direction, main files changed, validation performed, and assumptions that materially affect the design system.

## Stop Rules

Stop when the interface is implemented, reachable states and responsive behavior are handled, and the most relevant validation has run through the real route and interaction when accessible. If validation cannot run, report why and name the next best check.
