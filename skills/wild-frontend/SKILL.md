---
name: wild-frontend
description: Create bold, unconventional frontend designs when product conventions are intentionally not the goal.
disable-model-invocation: true
---

# Wild Frontend

Create highly original, production-grade frontend artifacts where memorability, concept, and visual ambition matter more than product consistency.

Build real working code, not just a description.

For multi-step work, start with a short user-visible update that names the concept or first implementation surface you are checking.

## Goal

Choose one strong visual concept and execute it with discipline. The result should be distinctive, cohesive, functional, responsive, and usable.

## Success Criteria

- The result is real working code in the requested stack.
- One concept drives typography, color, layout, surface, texture, and motion.
- The composition is deliberate at both page and detail scale: hierarchy, alignment, proximity, rhythm, and negative space give the concept structure.
- The interface is surprising and memorable without blocking usability.
- Important text is readable, core controls support keyboard use and visible focus, reduced-motion preferences are respected, and decorative effects do not interfere.
- Interaction states the task can reach and common viewport sizes are handled.
- Visual output is rendered or inspected when the environment allows it.

## Creative Direction

Use the requested direction and references as constraints, then make deliberate creative choices where the brief leaves room. Before implementing, commit to a concise direction:

- **Purpose**: what the interface does
- **Concept**: the central idea
- **Tone**: brutal, luxurious, playful, cinematic, industrial, editorial, organic, surreal, retro, ceremonial, or another clear flavor
- **World**: the visual universe it belongs to
- **Signature detail**: what someone will remember
- **Interaction style**: how it moves, responds, or reveals itself

Use [references/creative-moves.md](references/creative-moves.md) only when you need additional concept examples or design moves.

## Craft Standard

Work as a visual craftsperson. Experimentation raises the standard for execution: unusual composition, asymmetry, overlap, and expressive type must look authored rather than accidental.

- Build the composition before adding effects. Establish the focal point, reading order, visual anchors, balance, tension, and the path the eye follows through the page.
- Treat negative space as a shape and pacing device, not the area left after placing elements. Tune margins, gaps, density changes, and empty regions so they create rhythm and reinforce the concept.
- Apply enduring graphic-design principles deliberately: hierarchy, alignment, proximity, repetition, contrast, scale, balance, rhythm, and figure-ground. Breaking a convention should create a specific visual or functional effect.
- Treat typography as both language and form. Refine measure, leading, tracking, wrapping, baseline relationships, and optical alignment; do not let dramatic type become careless type.
- Inspect the artifact at both scales: zoom out for silhouette, composition, and distribution of space; zoom in for edges, joins, layers, icon-and-label relationships, and interaction details. Use visible discrepancies and the brief to choose the next refinement.

## Constraints

- Keep the primary action clear.
- Keep important text readable.
- Preserve responsive behavior and keyboard-accessible controls when interactive.
- Provide usable loading, empty, and error states when relevant.
- Use accessible focus treatment and reasonable contrast for core content.
- Respect reduced-motion preferences. Reduce or replace nonessential motion while preserving content, controls, and understandable state changes.
- Avoid broken layouts at common viewport sizes.
- Do not let decorative effects block usability.

Question habitual choices such as centered cards, predictable heroes, timid palettes, purple/blue gradients on white, or generic fonts when they lack a connection to the concept. These are not aesthetic bans: follow a requested direction even when it uses a familiar treatment. Use creative freedom to develop the brief rather than replace it, and remove decoration or competing ideas that weaken it.

## Implementation Style

Write real working code in the requested stack: HTML/CSS/JS, React, Vue, Tailwind, CSS modules, SVG, Canvas, CSS animations, or component-local styling.

You may create one-off components, custom CSS, unusual layout systems, decorative layers, and bespoke interactions. Keep the code understandable enough to modify.

## Final Verification

Render the actual artifact with representative content. Inspect the full composition and close details at common viewport sizes: focal order, alignment anchors, negative space, section rhythm, text wrapping, optical balance, edge treatments, and interaction states. Responsive layouts should recompose intentionally rather than merely shrink or stack.

For animated work, inspect both the intended motion and the reduced-motion alternative. Confirm that essential content and controls remain available and that state changes still make sense.

A build or typecheck does not prove visual quality. Before each refinement, identify the visible discrepancy or unmet part of the brief it should address, then inspect the affected result. Continue while material problems remain in the concept's execution, readability, interaction, or responsiveness. If the artifact cannot be rendered, report that gap and the next best check.

## Output

Lead with the completed result, then report the concept, signature design moves, changed files, and validation performed.

## Stop Rules

Stop when the working artifact satisfies the brief, material visible problems are resolved, and relevant viewport, interaction, and motion checks are complete or their limits are stated. Do not keep redesigning a result that meets those conditions merely because another stylistic treatment is possible.
