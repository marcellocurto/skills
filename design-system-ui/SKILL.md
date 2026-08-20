---
name: design-system-ui
description: Design and implement production frontend UI that extends an existing product, codebase, component library, or design system. Use when explicitly invoked for polished product UI that should preserve local patterns.
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
- States the task can actually reach are handled, such as loading, empty, error, disabled, selected, focused, hovered, active, success, destructive, long content, and small screens. States are not invented merely for completeness.
- Responsive behavior is checked for common viewport sizes.
- Validation is run when available. When visual quality matters and the environment allows it, inspect the result through the real application route and interaction at the relevant viewports before finalizing.

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

## Output

When implementing, provide scoped code that is ready to run in the user's stack. In the final response, lead with the completed result, then name the product-aware direction, main files changed, validation performed, and assumptions that materially affect the design system.

## Stop Rules

Stop when the interface is implemented, reachable states and responsive behavior are handled, and the most relevant validation has run through the real route and interaction when accessible. If validation cannot run, report why and name the next best check.
