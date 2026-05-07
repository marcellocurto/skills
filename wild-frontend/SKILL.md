---
name: wild-frontend
description: Explicit-only skill for unconstrained, highly creative frontend design. Use only when the user explicitly says to use wild-frontend or asks to invoke this exact skill. Do not trigger automatically for normal frontend, styling, beautification, product UI, design-system, or production polish requests.
---

# Wild Frontend

Create highly original, production-grade frontend artifacts that avoid generic AI aesthetics. This is for interfaces where memorability, concept, and visual ambition matter more than product consistency.

Use this skill only when explicitly invoked. Build real working code, not just a description. Push the art direction hard, but keep the result functional, responsive, and usable.

## Goal

Treat the interface as a designed artifact, not a default product surface.

Choose one strong concept and execute it with discipline. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity. The result should feel like a specific visual world brought to life in code.

Do not hold back. Strong creative frontend work is possible when the desired outcome, constraints, and concept are clear.

## Success Criteria

- The result is real working code, not a design description.
- One distinct visual concept drives typography, color, layout, surface, texture, and motion.
- The interface is surprising, cohesive, functional, memorable, responsive, and usable.
- Important text is readable, core controls are accessible enough for the task, and decorative effects do not block usability.
- The result includes relevant interaction states and works at common viewport sizes.
- Visual output is rendered or inspected when the environment allows it.

## Creative Direction

Before implementing, commit to a distinct direction:

- **Purpose** — What does this interface do, and who is it for?
- **Concept** — What is the central idea?
- **Tone** — Pick a strong flavor: brutal, luxurious, playful, cinematic, industrial, editorial, organic, surreal, retro, ceremonial, etc.
- **World** — What visual universe does it belong to?
- **Constraints** — Stack, performance, accessibility, responsive needs, and any user requirements.
- **Differentiation** — What makes this unforgettable instead of merely polished?
- **Signature detail** — What is the one thing someone will remember?
- **Interaction style** — How should it move, respond, or reveal itself?

Possible directions:

- brutalist editorial
- cinematic sci-fi console
- playful toy interface
- dense cyberpunk dashboard
- luxury fashion microsite
- organic botanical system
- retro operating system
- maximalist poster layout
- generative art interface
- analog paper-and-ink workspace
- museum exhibit panel
- arcade machine UI
- surreal glass-and-light environment
- industrial control room
- weird experimental zine
- monochrome Swiss poster grid
- tactile scrapbook interface

Do not mix every idea together. Pick one and make every visual choice serve it.

## Design Moves

Use bold, intentional choices across the full interface. These are possible moves, not a checklist; choose the few that best express the concept.

### Typography

Choose typography with character. Avoid defaulting to Arial, Roboto, Inter, or system fonts unless the concept makes that choice intentional.

Create identity through:

- oversized display headlines
- unusual scale contrast
- expressive letter spacing
- editorial pull quotes
- compressed labels
- huge numbers
- vertical or rotated text
- mono/typewriter details
- delicate serif contrast
- brutal utility typography
- poster-like hierarchy

If external fonts are unavailable, create distinction through scale, weight, spacing, casing, rhythm, and layout.

### Color

Build a committed palette. Color should create a world, not decorate components.

Use:

- one dominant atmosphere
- one or two sharp accents
- dramatic contrast
- monochrome with a single signal color
- acidic highlights
- muted editorial tones
- deep cinematic darks
- warm analog neutrals
- strange but controlled gradients
- status colors only when meaningful

Avoid timid evenly distributed palettes and interchangeable purple-gradient-on-white aesthetics.

### Layout

Break predictable SaaS structure while preserving comprehension.

Use:

- asymmetry
- overlapping layers
- diagonal flow
- poster composition
- split screens
- dense information clusters
- oversized hero sections
- floating panels
- editorial columns
- irregular grids
- anchored navigation
- dramatic negative space
- layered foreground/background systems

The layout should guide attention and feel custom to the concept.

### Surface and Texture

Make the screen feel physically or atmospherically specific.

Use:

- grain or noise
- glows and radial light
- scanlines
- paper texture
- glass layers
- hard shadows or soft depth
- geometric patterning
- borders and frames
- masks and cutouts
- ornamental dividers
- illustrated empty states
- custom badges and labels

Effects should reinforce the chosen concept, not appear as random decoration.

### Motion

Use motion as part of the design language.

Consider:

- staged entrance sequences
- hover distortions
- reveal masks
- sliding panels
- kinetic typography
- parallax depth
- animated gradients
- pulsing status elements
- cursor-follow effects
- springy interactions
- cinematic transitions

Prefer a few memorable motions over constant noise. Respect reduced-motion preferences when practical.

## Complexity Should Match the Vision

Match implementation complexity to the chosen aesthetic.

- Maximalist concepts may need layered CSS, SVG, animation, generated elements, and rich visual systems.
- Minimalist concepts need restraint, precision, spacing, typography, alignment, and subtle interaction detail.
- Experimental concepts can use one-off components and bespoke effects, but the code should still be understandable.

Elegance comes from executing the concept well, not from adding more effects.

## Constraints

Wild does not mean careless. Ensure:

- clear primary action
- readable important text
- responsive behavior
- usable loading/empty/error states when relevant
- accessible focus treatment
- reasonable contrast for core content
- keyboard-accessible controls when interactive
- no broken layout at common viewport sizes
- no decorative effect that blocks usability

Avoid generic AI aesthetics, safe SaaS dashboard defaults, bland centered cards, predictable hero sections, timid palettes, overused purple/blue gradients on white, generic font choices without intent, cookie-cutter component layouts, random decoration without a concept, copying the existing codebase style unless requested, apologizing for being bold, or making every generated design feel the same.

## Implementation Style

Write real working code in the requested stack: HTML/CSS/JS, React, Vue, Tailwind, CSS modules, SVG, Canvas, CSS animations, or component-local styling.

You may create one-off components, custom CSS, unusual layout systems, decorative layers, and bespoke interactions. Do not feel constrained by existing product components unless the user specifically requests compatibility.

When producing code:

- implement the actual interface, not a design description
- include the visual system directly in the code
- make the direction obvious from the result
- include responsive behavior and interaction states
- keep the code maintainable enough to modify

When explaining the result, briefly name the concept and signature design moves.

## Output

Briefly report the concept, signature design moves, changed files, and validation performed.

## Stop Rules

Stop when the concept is implemented as working code, common viewport behavior is checked, and the artifact has been rendered or the best available validation has run. If validation cannot run, report why and name the next best check.
