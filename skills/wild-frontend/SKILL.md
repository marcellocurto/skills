---
name: wild-frontend
description: Create bold, unconventional frontend designs when product conventions are intentionally not the goal.
disable-model-invocation: true
---

# Wild Frontend

Build working frontend code around a distinctive visual concept. This skill prioritizes originality and memorability over matching an existing product style.

For multi-step work, start with a short update naming the concept or the first part of the interface you are checking.

## Goal

Choose one concept that guides typography, color, layout, texture, and motion. Make the result memorable while keeping the main task easy to understand and complete.

## Creative Direction

Use the requested direction and references as constraints, then make deliberate creative choices where the brief leaves room. Before implementing, commit to a concise direction:

- **Purpose**: what the interface does
- **Concept**: the central idea
- **Tone**: brutal, luxurious, playful, cinematic, industrial, editorial, organic, surreal, retro, ceremonial, or another clear flavor
- **References**: visual sources, materials, or settings that inform the design
- **Signature detail**: what someone will remember
- **Interaction style**: how it moves, responds, or reveals itself

Use [references/creative-moves.md](references/creative-moves.md) only when you need additional concept examples or design moves.

## Craft Standard

Use unusual composition, asymmetry, overlap, and expressive type for a specific visual effect. Check their alignment, spacing, and readability as carefully as a conventional layout.

- Build the composition before adding effects. Establish the focal point, reading order, visual anchors, balance, tension, and the path the eye follows through the page.
- Treat negative space as a shape and pacing device, not the area left after placing elements. Tune margins, gaps, density changes, and empty regions so they create rhythm and reinforce the concept.
- Apply enduring graphic-design principles deliberately: hierarchy, alignment, proximity, repetition, contrast, scale, balance, rhythm, and figure-ground. Breaking a convention should create a specific visual or functional effect.
- Treat typography as both language and form. Refine measure, leading, tracking, wrapping, baseline relationships, and optical alignment; do not let dramatic type become careless type.

## Constraints

- Keep the primary action clear.
- Keep important text readable.
- Make layouts work at common viewport sizes and provide keyboard access to interactive controls.
- Provide usable loading, empty, and error states when relevant.
- Use accessible focus treatment and reasonable contrast for core content.
- Respect reduced-motion preferences. Reduce or replace nonessential motion while preserving content, controls, and understandable state changes.
- Do not let decorative effects block usability.

Question habitual choices such as centered cards, predictable heroes, timid palettes, purple/blue gradients on white, or generic fonts when they lack a connection to the concept. These are not aesthetic bans: follow a requested direction even when it uses a familiar treatment. Use creative freedom to develop the brief rather than replace it, and remove decoration or competing ideas that weaken it.

## Implementation Style

Use the requested stack. One-off components, custom CSS, unusual layouts, decorative layers, and custom interactions are allowed when they serve the concept. Keep the code understandable enough to modify.

## Final Verification

Render the actual artifact with representative content. Inspect the full composition and close details at common viewport sizes: focal order, alignment anchors, negative space, section rhythm, text wrapping, optical balance, edge treatments, and interaction states. Responsive layouts should recompose intentionally rather than merely shrink or stack.

Use the interface with the keyboard and confirm that focus remains visible and the controls work. Exercise the loading, empty, and error states that can actually occur.

For animated work, inspect both the intended motion and the reduced-motion alternative. Confirm that essential content and controls remain available and that state changes still make sense.

A build or typecheck does not prove visual quality. Before each refinement, identify the visible discrepancy or unmet part of the brief it should address, then inspect the affected result. Continue while material problems remain in the concept's execution, readability, interaction, or responsiveness. If the artifact cannot be rendered, report that gap and the next best check.

## Output

Lead with the completed result, then report the concept, signature design moves, changed files, and validation performed.

## Stop Rules

Stop when the working artifact satisfies the brief, material visible problems are resolved, and relevant viewport, interaction, and motion checks are complete or their limits are stated. Do not keep redesigning a result that meets those conditions merely because another stylistic treatment is possible.
