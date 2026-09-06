# Logic Prototype

For questions about business logic, state transitions, or data shape, a self-contained HTML demo is a useful default when someone needs to explore the behavior by clicking through scenarios. Use a simpler script, fixture, or runnable sample when it answers the question more directly, as described in [SKILL.md](SKILL.md).

Because it's one file with nothing to install, you can hand it to a non-developer (a designer, a PM, a domain expert) and let them feel the model for themselves. So it speaks their language, not the code's.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where someone wants to **press buttons and watch state change**.

If the question is "what should this look like," this is the wrong branch. Use [UI.md](UI.md).

## Process

### 1. State the question

State the model and the question briefly in the artifact or its handoff. For an interactive HTML demo, put that explanation in a visible intro so someone opening it later knows what to explore.

### 2. Isolate the logic in a portable module

Keep the logic being evaluated separate from the demonstration UI so its inputs and state transitions are easy to inspect. For the HTML default, a small module in a `<script>` block is usually enough. The logic remains prototype code even when its shape may inform a later implementation.

The right shape depends on the question:

- **A pure reducer**: `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine**: explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state, just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick the shape that fits the question. For a state-model experiment, keep DOM access in the demonstration UI and let it call the logic through explicit actions. If the question depends on browser behavior or another real runtime, preserve that dependency rather than replacing it with a pure model that cannot answer the question.

### 3. Build the demonstration

For a standalone demo, prefer one HTML file with inline CSS and JavaScript that opens without setup. Use the project's runtime when the question requires it or the user requested that format.

Match the explanation to the audience. For a non-developer, label actions and state in domain language and explain what changes. A technical sample may expose the actual types, inputs, or API calls under discussion.

For an interactive HTML demo, use the parts of this layout that help answer the question:

1. **Title and one-line explanation** of what this demo lets you explore (the question from step 1).
2. **Current state**: the full relevant state, rendered as a readable panel (labelled fields, not a raw JSON dump), re-rendered after every click so the change is visible. Where it helps a non-developer follow, call out what just changed.
3. **Free-play buttons**: one button per action, always available, so anyone can poke at the model in any order. Each click dispatches its action and re-renders the state.
4. **Guided walkthroughs**: a set of **scenarios**, one per tab. Each tab holds a short plain-language description of the scenario (the situation it sets up and what to watch for) and underneath it, the ordered **buttons to press** for that scenario. Each step is a real button: clicking it performs that action and moves to the next step. Starting a walkthrough resets to a known initial state so the scenario runs the same way every time.

Choose scenarios that distinguish the behavior under discussion. Guided tabs help compare several sequences; a single scenario or direct output may be enough for a narrow question.

Keep it beautiful but restrained: clean typography, generous spacing, one accent colour. No animations, no gimmicks: nothing that competes with the state and the buttons.

### 4. Hand it over

Send them the file, or open it for them. They'll click through the walkthroughs and free-play whenever they get to it; the interesting moments are when they say "wait, that shouldn't be possible" or "huh, I assumed X would be different"; those are the bugs in the _idea_, which is the whole point. If they want new actions or a new scenario, add them. Prototypes evolve.

### 5. Report the answer

Report which scenarios were exercised, what they establish, and which domain decisions remain open. Follow the completion and authorization boundaries in [SKILL.md](SKILL.md). Preserve the artifact for inspection; incorporating its logic into production or recording it in Git or an issue is conditional on authorization.

## Anti-patterns

- **Don't build a test suite merely to harden the prototype.** Use a focused assertion or executable example when it directly answers the question.
- **Don't wire it to the real database.** Use in-memory state unless the question is specifically about persistence.
- **Don't generalise.** No "what if we wanted to support X later." The prototype answers one question.
- **Don't hide the behavior inside demonstration plumbing.** Keep the state and transitions inspectable without requiring the reader to reconstruct the UI.
- **Don't add runtime setup without a reason.** Prefer the standalone file when portability matters, and the real runtime when its behavior is being evaluated.
- **Don't treat demonstrated logic as production-ready.** Carry the evidence into any authorized implementation and verify the resulting production path.
