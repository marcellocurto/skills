---
name: design-system-ui
description: Build polished production UI that extends a product's existing design system and patterns.
disable-model-invocation: true
---

# Design System UI

Build UI that fits the product's existing components, visual style, and interaction patterns.

For multi-step work, start with a short user-visible update that names the product context you are inspecting first.

## Goal

Make the requested screen or component easier to read and use while keeping it consistent with the rest of the product. Use hierarchy, grouping, spacing, and interaction feedback to support its main task.

## Context Budget

Before coding, inspect only the context needed to make the UI fit:

- nearby pages with a similar purpose
- shared components and page shells
- tokens, theme files, Tailwind/CSS config, and typography
- spacing, radius, borders, shadows, surfaces, icons, and motion
- existing loading, empty, error, disabled, focus, and responsive patterns

Stop discovery once the product context, reusable primitives, styling system, and validation path are clear enough to implement. Continue only when a missing pattern would materially affect correctness, visual fit, or accessibility.

## Product Direction

For an ordinary production change, reuse the product's established direction and resolve only the choices needed for the requested surface. A small adjustment does not require a new concept, palette, or signature detail.

For a new screen or substantial redesign, establish a concise direction from the available context:

- **Purpose**: what job the interface does
- **User**: who uses it and what they are deciding or accomplishing
- **Existing patterns**: layout, typography, colors, and interactions to reuse
- **Useful improvement**: a specific change that helps the user complete the task
- **Distinctive detail, when useful**: a detail requested or supported by the brief; do not add decoration just to make the screen different

Use [references/design-moves.md](references/design-moves.md) only when you need more examples for typography, layout, color, surface, motion, or states.

## Craft Standard

Use hierarchy, alignment, grouping, contrast, and space to make the requested surface clear in its product context. For page-level work, establish composition before polishing details; for a component change, inspect its fit with the surrounding page without redesigning that page. Applying the right tokens alone does not establish visual quality. Use the visual checks below to guide refinement.

## Constraints

- Write real working frontend code that follows project conventions.
- Treat user-supplied copy, business claims, interaction meaning, screenshots, and existing information architecture as product constraints unless the user asks to reconsider them. Do not solve a presentation problem by deleting required content, weakening claims, or changing product semantics.
- Keep changes within the requested screens and components. Change a shared primitive only when it is the demonstrated cause or the requested result genuinely requires it, then verify the affected consumers.
- Prefer existing primitives, tokens, icon sets, animation utilities, accessible HTML, keyboard-friendly interactions, responsive behavior, clear component structure, and scoped styling.
- Add new visual primitives only when they improve the design and could fit naturally into the product system.
- Do not introduce asynchronous behavior, loading states, or layout shifts for static or synchronous content.
- Avoid arbitrary custom styles, decoration without product purpose, extra components when existing primitives fit, centered-card layouts by default, turning every content group into a bordered card, false interaction affordances, timid evenly distributed color, and purple-gradient polish pasted onto unrelated products.

## When There Is No Clear Design System

Define only the missing visual choices needed for the requested surface, such as color roles, type hierarchy, spacing, control treatment, and responsive or interaction behavior. A small task does not require a complete new design system.

Make it coherent through a few strong choices rather than many unrelated effects.

## Visual Verification

Inspect the implementation through the real application route and interaction when accessible. Use these checks during refinement and for the final result; reuse observations when the relevant implementation, content, and state have not changed:

- Use representative data volume, realistic localized copy, long values, and the scale conditions that could change the layout or interaction model.
- Check responsive behavior at relevant viewport sizes and reachable states introduced or affected by the work, including keyboard and focus behavior. Do not invent states merely for completeness.
- Inspect both composition and details: focal order, grouping, density, whitespace, alignment, nested padding, text wrapping, baselines, icon-and-label pairs, and control dimensions. Compare with adjacent product screens for consistent typography, surfaces, and interaction language.
- Check that added surfaces, icons, badges, and feedback communicate a useful relationship or state. Resolve accidental gaps, layout shifts, false affordances, and decoration that interferes with the task.

Run applicable code validation as well, but do not treat a build, typecheck, or component-level test as proof of visual quality. If the real route cannot be inspected, report the gap and the next best verification instead of claiming the UI is fully verified.

## Output

When implementing, provide scoped code that is ready to run in the user's stack. In the final response, lead with the completed result, then summarize material design choices, main files changed, validation performed, and assumptions that affect the result. Do not invent a new concept to describe a routine change.

## Stop Rules

Stop when the requested interface is implemented, material discrepancies affecting behavior, usability, accessibility, responsiveness, or product fit are resolved, and applicable verification is complete or its limits are stated. Further refinement needs a concrete remaining discrepancy; do not keep changing placements or adding embellishments merely to pursue subjective perfection.
