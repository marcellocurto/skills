# UI Prototype

Build a UI prototype that makes a visual or interaction question concrete. A preview in product context is a useful default; add switchable variants when comparison will help the user choose. A single rendition is enough when the task is to evaluate one proposed design.

If the question is about logic/state rather than what something looks like, this is the wrong branch. Use [LOGIC.md](LOGIC.md).

## When this is the right shape

- "What should this page look like?"
- "I want to see a few options for this dashboard before committing."
- "Try a different layout for the settings screen."
- Comparing visual choices that are difficult to judge from prose alone.

## Choose the preview location

Use nearby screens, realistic content, and representative density when the question depends on how a design fits the product. Prefer an existing page when it provides that context without unnecessary integration work. Follow the requested medium and choose a separate preview when isolation makes the experiment easier to run or share.

### Existing page

An opt-in preview on the existing route can preserve the real page shell, data shape, and density. A `?variant=` URL search parameter is useful when alternatives need shareable links. Preserve existing routing, authentication, and ordinary rendering outside the local preview.

For a new section or step within an existing flow, preview it in the host page when that context affects the decision.

### Separate preview

Use a temporary route, standalone mockup, or component preview when the design has no natural host, the user requested an independent artifact, or integration work would not help answer the question.

For a route, follow project conventions and name it clearly as a prototype. Reproduce enough surrounding context to judge the design; an empty fixture may conceal density or layout problems.

## Process

### 1. State the question and choose the scope

Follow the user's requested number of variants. Otherwise build the smallest set that distinguishes the open choices: one for evaluating a specific direction, multiple when comparison is the question. Do not create alternatives to meet a quota.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Compare a sidebar and a tabbed layout for the settings page, using opt-in previews on `/settings`."

This works whether the user is here to push back or not.

### 2. Build the relevant design or alternatives

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library / styling system (TailwindCSS, shadcn, MUI, plain CSS, whatever).
- Clear names for the alternatives, including component names when the artifact uses components.

Make alternatives differ along the dimension being evaluated. For a layout decision, vary hierarchy, composition, or affordances enough to expose the tradeoff. For a typography or palette decision, keep the structure stable so the visual difference can be judged. Do not redesign unrelated aspects merely to make variants look different.

### 3. Make comparison easy when needed

For multiple variants, choose a comparison surface that suits the question: a route switcher, tabs, side-by-side previews, or separate links. Skip comparison controls for a single rendition. This example shows an opt-in route preview for two alternatives; adapt the preview gate and routing to the project:

```tsx
// pseudo-code, adapt to the project's framework
const variant = searchParams.get('variant');
if (!isPrototypePreviewEnabled || (variant !== 'A' && variant !== 'B')) {
  return <ExistingPage {...data} />;
}
return (
  <>
    {variant === 'A' ? <VariantA {...data} /> : <VariantB {...data} />}
    <PrototypeSwitcher variants={['A', 'B']} current={variant} />
  </>
);
```

For an existing page, preserve the data and context relevant to the experiment; only the previewed subtree needs to change.

For a separate preview, supply representative fixtures and reuse the comparison controls only when needed.

### 4. Optional floating switcher

When a floating switcher is the chosen comparison surface, use a small bar with:

- **Left arrow**: cycles to the previous variant (wraps around).
- **Variant label**: shows the current variant key and, if the variant exports a name, that name too. e.g. `B (Sidebar layout)`.
- **Right arrow**: cycles forward (wraps around).

Behaviour:

- Clicking an arrow updates the URL search param (use the framework's router, e.g. `router.replace` on Next, `navigate` on React Router, etc) so the variant is shareable and reload-stable.
- Keyboard: `←` and `→` arrow keys also cycle. Don't intercept arrow keys when an `<input>`, `<textarea>`, or `[contenteditable]` is focused.
- Visually distinct from the page (e.g. high-contrast pill, subtle shadow) so it's obviously not part of the design being evaluated.
- Gate the whole preview, including its variants and controls, using the project's local preview convention. Hiding the bar alone must not leave experimental rendering active in ordinary use.

Keep the switcher with the prototype. Share it across previews only when the experiment actually needs that reuse.

### 5. Hand it over

Open or link the preview and explain how to inspect any alternatives. Exercise the interactions and viewport conditions needed to judge the question. Report observed differences and limitations, and distinguish your recommendation from a choice the user has actually made.

### 6. Record the conclusion

State what the prototype demonstrated, any selected direction and its rationale, and the decision still open if the user has not chosen. Follow the completion and authorization boundaries in [SKILL.md](SKILL.md).

If production integration is authorized, adapt the selected direction into the existing page or a real route as appropriate, then verify it under production requirements. Remove preview scaffolding as part of that integration. Preserve or archive the prototype only in the location and form authorized; there is no mandatory throwaway-branch commit or issue update.

## Anti-patterns

- **Variants that do not distinguish the decision.** A layout comparison needs meaningful structural differences; a palette comparison does not.
- **Sharing code that forces the answer.** Reuse stable context, but keep each alternative free to change the dimension being evaluated.
- **Wiring variants to real mutations.** Read-only prototypes are fine. If a variant needs to mutate, point it at a stub: the question is "what should this look like", not "does the backend work".
- **Treating a preferred variant as authorization to ship it.** Prototype code was written for an experiment; production integration requires authorization and appropriate implementation and verification.
