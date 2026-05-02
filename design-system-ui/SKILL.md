---
name: design-system-ui
description: Design and implement polished frontend UI that feels native to the existing product, codebase, component library, and design system. Use for normal production frontend work where the result should extend real project patterns rather than invent a disconnected visual direction.
disable-model-invocation: true
---

# Frontend Design

Create polished, production-grade frontend interfaces with strong visual direction and real working code.

The goal is to make the UI feel like the **best-designed version of this product**, not like a random standalone concept. Be creative, but ground every design choice in the codebase, design system, component library, and surrounding product experience.

## Design Principle

Use the existing product as the creative material.

A great result should feel:

- native to the app
- visually intentional
- more refined than the surrounding UI
- consistent with existing components and tokens
- memorable because of hierarchy, composition, detail, and interaction quality

Do not default to bland consistency. Extend the system with taste.

## Design Discovery

Before coding, inspect the project when available.

Look for:

- existing pages with similar purpose
- shared components such as `Button`, `Card`, `Input`, `Dialog`, `Table`, `Badge`, `Tabs`, `Tooltip`
- layout primitives and page shells
- design tokens, CSS variables, Tailwind config, theme files, or style constants
- typography scale, font usage, font weights, and heading patterns
- spacing, radius, border, shadow, and surface conventions
- icon library and illustration style
- motion patterns and interaction states
- responsive breakpoints
- empty, loading, error, and disabled states
- accessibility patterns

Build from these patterns first. If the codebase already has usable primitives, compose them into something stronger instead of replacing them with one-off markup.

## Design Thinking

Before implementing, form a short design direction.

Answer these silently or briefly:

- **Purpose** — What job does this interface do?
- **User** — Who is using it, and what are they trying to decide or accomplish?
- **Product context** — Is this a dashboard, marketing surface, admin tool, editor, onboarding flow, data view, commerce page, or content experience?
- **System language** — What does the existing UI already communicate: calm, dense, playful, technical, premium, utilitarian, editorial, enterprise, minimal?
- **Upgrade move** — What can be made more distinctive while still fitting the product?
- **Signature moment** — What is the one detail users will remember?

Choose a clear direction that belongs in the product, for example:

- a calmer, more focused settings page
- a denser operations dashboard with stronger scan paths
- a more editorial landing section using the existing type scale
- a premium checkout flow with better hierarchy and trust cues
- a playful empty state that still uses the product’s components
- a sharper analytics view with more intentional data grouping
- a tactile card layout with refined depth, borders, and hover states
- a command-center interface for high-information workflows
- a warm onboarding flow with better progression and reassurance

## Creative Moves to Use

Use creativity through product-aware design moves.

### Typography

Use the existing font system unless the task is greenfield or explicitly allows new typography.

Create distinction through:

- stronger heading hierarchy
- better line length
- tighter or looser tracking where appropriate
- deliberate font weight contrast
- eyebrow labels
- section headers
- numeric emphasis for metrics
- improved content rhythm
- clearer primary and secondary text relationships

### Layout and Composition

Make the interface feel designed through structure.

Use:

- clear visual hierarchy
- strong alignment
- intentional whitespace
- grouped sections
- asymmetric but balanced layouts
- split panes
- sticky action areas
- dashboard grids
- editorial hero sections
- progressive disclosure
- compact density for expert workflows
- spacious layouts for onboarding or marketing
- cards and panels that create meaningful information zones

Prefer composition that helps the user understand what matters first.

### Color and Theme

Use existing semantic tokens and palette first.

Create polish through:

- better contrast between primary, secondary, and muted content
- one confident accent area
- semantic status colors
- subtle surface layering
- restrained gradients when they fit the product
- tinted panels for emphasis
- color used to guide attention, not decorate everything

If the design system is minimal, introduce a small, coherent local palette using CSS variables or existing token patterns.

### Surface and Detail

Use visual detail to clarify structure and make the UI feel finished.

Good details include:

- refined borders
- soft or crisp shadows matching the product style
- layered cards
- subtle dividers
- inset panels
- hover elevation
- selected states
- focus rings
- empty-state illustrations or icons
- badges and metadata
- tasteful background texture or pattern when appropriate
- clear affordances for interactive elements

Details should make the interface easier to read, trust, or use.

### Motion and Interaction

Use motion to explain state changes and add quality.

Prefer:

- fast, subtle transitions
- hover and press states
- staged entrance for important content
- smooth expand/collapse
- loading skeletons
- optimistic state feedback
- scroll or reveal effects only for expressive surfaces
- reduced-motion friendly behavior

Motion should support comprehension. One well-placed interaction is better than many decorative animations.

### States

Design the complete experience, not just the happy path.

Include useful handling for:

- loading
- empty
- error
- disabled
- selected
- focused
- hovered
- active
- success
- destructive actions
- long content
- small screens

A production-grade UI feels considered in every state.

## Implementation Guidelines

Write real, working frontend code that follows the project’s conventions.

Prefer:

- existing components and primitives
- existing tokens and theme variables
- existing layout patterns
- existing icon sets
- existing animation utilities
- accessible HTML
- keyboard-friendly interactions
- responsive behavior
- clear component structure
- scoped styling
- reusable local abstractions when helpful

Add new visual primitives only when they improve the design and can fit naturally into the system.

If adding a new style pattern, make it look like something the product could adopt elsewhere.

## When the Codebase Has No Clear Design System

If the project is greenfield or visually inconsistent, create a small local design direction.

Define:

- a compact color system
- a typography hierarchy
- spacing rhythm
- radius and shadow rules
- button/input/card treatment
- responsive layout behavior
- interaction state conventions

Keep it coherent and reusable. Make the design distinctive through a few strong choices rather than many unrelated effects.

## Output Expectations

When implementing, provide scoped code that is ready to run in the user’s stack.

When explaining the result, briefly mention:

- the design direction
- which existing patterns or components it uses
- what visual upgrades were made
- any assumptions about the design system
- any follow-up refinements worth considering

## Quality Bar

The finished UI should feel like it belongs in the product, but with better composition, clearer hierarchy, more thoughtful states, and stronger visual polish than a default implementation.

It should be distinctive because it is deeply fitted to the product context — not because it ignores it.