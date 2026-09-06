---
name: prototype
description: Build a temporary prototype to answer a specific design or behavior question.
---

# Prototype

A prototype is a temporary artifact that answers a specific design or behavior question. Build only what makes that question possible to judge.

## Choose the artifact

Identify the question, who will judge the result, and which observation or comparison would help them decide. Use the user's prompt and relevant existing code. Ask only when unresolved ambiguity would materially change the artifact; otherwise state a reasonable assumption and proceed.

- **Logic, state, or data shape:** [LOGIC.md](LOGIC.md) describes a shareable HTML demo with visible state and guided scenarios, useful when someone needs to explore behavior interactively.
- **Appearance or interaction:** [UI.md](UI.md) describes previews in product context and ways to compare alternatives when a visual choice remains open.

These are defaults, not required formats. A script, fixture, runnable sample, or single mockup may answer a narrower question more directly. Preserve the user's requested medium and stack. Use one artifact or variant when it can answer the question; add alternatives only to compare meaningful choices, following any count the user requested.

## Build and demonstrate

1. **Keep it identifiable and contained.** Use the requested location or an existing prototype convention. Place it near the relevant module or page when product context helps; use a scratch location for an independent artifact. Mark it as a prototype and keep changes limited to what the experiment needs.
2. **Make it easy to run.** Prefer one file to open or one existing project command. Give exact launch instructions appropriate to the chosen format.
3. **Use temporary state.** Default to memory or fixtures. When persistence is the question, use a clearly identified scratch database or local file. A prototype request does not authorize production or external mutations.
4. **Match fidelity to the question.** Build the behavior, visual detail, and error handling needed to judge it. Avoid production hardening, speculative abstractions, and test infrastructure that do not help the experiment.
5. **Expose the evidence.** Show the state, output, or visual differences that matter. Exercise the relevant scenarios and record what they demonstrate. Distinguish observed results from assumptions and checks that could not run.

## Finish within scope

Deliver the artifact, how to run or inspect it, and the conclusion supported by the demonstration. If choosing a design or settling domain behavior still requires the user's judgment, explain the remaining decision rather than declaring it settled. Stop when the requested artifact and available evidence have been delivered.

Production integration, commits, pushes, and issue updates require authorization for those actions. A prototype request or favorable feedback alone does not authorize them. Honor authorization already given without asking for it again. When promotion is authorized, adapt and verify the chosen design under the project's production requirements; a successful demonstration does not establish production readiness.

Keep the delivered prototype available for inspection. Archive it to a branch, publish a context pointer, or remove it only when that disposition is part of the authorized work.
