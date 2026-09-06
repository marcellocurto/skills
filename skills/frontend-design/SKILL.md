---
name: frontend-design
description: Design and implement distinctive web interfaces with typography, composition, and visual identity grounded in the product and audience. Covers new UI and visual redesigns, rather than interface audits or behavior-only fixes.
disable-model-invocation: true
---

# Frontend Design

Deliver working UI whose visual choices belong to the subject, audience, and task. Preserve the requested stack, scope, brand direction, and established product patterns unless the brief calls for changing them.

## Establish what the interface needs to express

Read the brief, relevant existing screens, and available content before choosing an aesthetic. Identify the audience, the main action, and the subject-specific details that can give the interface its character. Ask when missing product context would change the design substantially; otherwise state a reasonable assumption and proceed.

Describe the intended visual direction briefly before implementation: the focal point, type roles, palette, and composition. Record reusable choices in the project's existing tokens or a small set of CSS variables. Match the amount of planning to the scope; a component does not need a page design exercise.

Check whether the same direction could be applied unchanged to an unrelated product. If so, replace the interchangeable choices with ones supported by this brief. Follow an explicitly requested aesthetic even when it is familiar.

## Make the content determine the form

- Give the most meaningful content the strongest visual presence. On a landing page, choose an opening treatment that introduces the subject directly; do not assume every page needs the same headline, metrics, and call-to-action arrangement.
- Build hierarchy through scale, alignment, grouping, and space before adding surface effects. Use containers and separators to communicate relationships. Number items only when their order matters.
- Choose typefaces for the product's character and reading conditions. Define clear roles and tune line length, leading, weight, and wrapping with representative content. Add a second family only when it has a distinct purpose.
- Make color roles explicit so emphasis remains selective. Avoid relying on habitual palettes, headline accents, uppercase labels, or identical cards to give unrelated projects the same appearance.
- Concentrate visual emphasis where it helps the interface communicate. Supporting areas should make that focal point easier to understand. Remove effects and decoration that compete with content.
- Use animation to explain interaction or direct attention at a meaningful moment. Avoid repeating entrance effects across every section; respect reduced-motion preferences.

Write UI copy in the product's voice for its actual audience. Use concrete content relevant to the subject; do not invent customer endorsements or product claims. Keep action names consistent through controls and feedback. Empty and error states should explain the situation and offer an appropriate next action. Conversational brevity preferences do not define the product's voice.

## Resolve the implementation visually

Build the requested interface with functioning interactions. Keep styling ownership clear so competing selectors do not accidentally override spacing or component states. Adapt the composition to narrow screens rather than merely reducing its size. Preserve readable contrast, semantic controls, visible keyboard focus, and keyboard access.

Render the result when the environment supports it and inspect representative wide and narrow viewports. Check the reading order, text wrapping, spacing, focal balance, and reachable interaction states. Correct visible discrepancies and remove details that dilute the chosen direction. A successful build alone does not establish visual quality.

Finish with the implemented result, the main design decisions, and the checks performed. Disclose any rendering or interaction checks that could not be completed.
