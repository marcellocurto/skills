# HTML Architecture Reports

Use this guide when the requested output or comparison benefits from an HTML artifact. Inline diagrams or prose may be a better fit for a compact review; choosing HTML is not a prerequisite for architectural analysis.

## Make the report portable

Create one HTML file with inline CSS and SVG, using system fonts by default. Opening the report must not depend on a CDN, remote stylesheet, font service, or diagram runtime. Links to source material may remain external; the report itself should still be readable offline.

If a diagram tool is already available, embed its rendered SVG. Otherwise draw the needed relationships with inline SVG or HTML/CSS. Do not place raw Mermaid markup in the file and assume the browser will render it. Use the host's Mermaid renderer for an inline answer when that capability is available.

Add inline JavaScript only when interaction helps inspect the architecture or compare alternatives. A static report does not need an application framework or build setup.

Save to the user's requested location, otherwise to a fresh file in the OS temp directory. Show it with an available artifact preview or provide a link and absolute path. Do not require a specific desktop opener.

## Explain each candidate

Lead with the concrete problem and the proposed change. For each candidate, include only the information needed to judge it:

- affected files or symbols and the caller trace or other evidence behind the finding
- the current maintenance or comprehension cost
- what ownership, caller responsibilities, or dependency relationships would change
- expected benefits, material tradeoffs, and contracts that must be preserved
- verification needed and uncertainty that could change the recommendation

Use short paragraphs when they explain a contract or tradeoff better than labels or bullets. Keep evidence with the claim it supports; do not compress away qualifications to fit a word limit. A diagram can show structure while the accompanying prose explains why it matters.

For discovery, identify the strongest candidate and why. For an already-selected target, focus on that change and the remaining design question; do not manufacture a candidate gallery or selection step.

## Choose diagrams for the relationship

- **Call or dependency graph:** show the handoffs a caller must understand and which become internal.
- **Sequence:** show ordering, coordination, or repeated work that the proposed design changes.
- **Ownership map:** show where data, policy, and invariants live before and after.
- **Before/after comparison:** keep the viewpoint and labels consistent so the structural difference is visible.

Use the same visual language for comparable relationships. Mix diagram types only when they explain different things; variety is not a goal. Do not imply that code size or rectangle area measures architectural quality. Name the decisions hidden from callers or the work no longer duplicated.

## Keep the report readable

Use clear hierarchy, readable text, and enough space for labels and explanations. Before/after diagrams can sit side by side on wide screens and stack on narrow ones. Avoid fixed heights that clip labels or force text to become too small.

Label nodes and relationships in the project's vocabulary. Distinguish observed structure from proposed structure. Use color as supporting emphasis, with text or line treatment conveying the same distinction. Include captions or accessible descriptions for diagrams whose meaning is not apparent from nearby prose.

Use ordinary architectural terms, including component, service, API, and boundary, when they match the repository. When using the `codebase-design` skill, let its distinctions clarify the explanation without replacing established names.

## Verify the delivered artifact

Open the actual report in an available preview or browser and inspect the diagrams, labels, before/after comparison, text wrapping, and source links. Check representative wide and narrow layouts when relevant. Confirm the file contains its required rendering assets and no unresolved placeholders.

Compare the report's claims and diagrams with the inspected code and the proposed design. A generated file is not proof that its rendering or architectural claims are correct. If visual inspection is unavailable, disclose the limitation and deliver the supported findings without claiming the report was rendered.
