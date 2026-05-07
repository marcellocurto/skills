---
name: wild-frontend
description: Explicit-only skill for unconstrained, highly creative frontend design. Use only when the user explicitly says to use wild-frontend or asks to invoke this exact skill. Do not trigger automatically for normal frontend, styling, beautification, product UI, design-system, or production polish requests.
---

# Wild Frontend

Create highly original, production-grade frontend artifacts where memorability, concept, and visual ambition matter more than product consistency.

Use this skill only when explicitly invoked. Build real working code, not just a description.

For multi-step work, start with a short user-visible update that names the concept or first implementation surface you are checking.

## Goal

Choose one strong visual concept and execute it with discipline. The result should be distinctive, cohesive, functional, responsive, and usable.

## Success Criteria

- The result is real working code in the requested stack.
- One concept drives typography, color, layout, surface, texture, and motion.
- The interface is surprising and memorable without blocking usability.
- Important text is readable, core controls are accessible enough for the task, and decorative effects do not interfere.
- Relevant interaction states and common viewport sizes are handled.
- Visual output is rendered or inspected when the environment allows it.

## Creative Direction

Before implementing, commit to a concise direction:

- **Purpose**: what the interface does
- **Concept**: the central idea
- **Tone**: brutal, luxurious, playful, cinematic, industrial, editorial, organic, surreal, retro, ceremonial, or another clear flavor
- **World**: the visual universe it belongs to
- **Signature detail**: what someone will remember
- **Interaction style**: how it moves, responds, or reveals itself

Use [references/creative-moves.md](references/creative-moves.md) only when you need additional concept examples or design moves.

## Constraints

- Keep the primary action clear.
- Keep important text readable.
- Preserve responsive behavior and keyboard-accessible controls when interactive.
- Provide usable loading, empty, and error states when relevant.
- Use accessible focus treatment and reasonable contrast for core content.
- Avoid broken layouts at common viewport sizes.
- Do not let decorative effects block usability.

Avoid generic AI aesthetics, safe SaaS defaults, bland centered cards, predictable hero sections, timid palettes, overused purple/blue gradients on white, generic font choices without intent, random decoration without a concept, and mixing too many visual ideas.

## Implementation Style

Write real working code in the requested stack: HTML/CSS/JS, React, Vue, Tailwind, CSS modules, SVG, Canvas, CSS animations, or component-local styling.

You may create one-off components, custom CSS, unusual layout systems, decorative layers, and bespoke interactions. Keep the code understandable enough to modify.

## Output

Briefly report the concept, signature design moves, changed files, and validation performed.

## Stop Rules

Stop when the concept is implemented as working code, common viewport behavior is checked, and the artifact has been rendered or the best available validation has run. If validation cannot run, report why and name the next best check.
