---
name: wayfinder
description: Break a large, uncertain effort into decision steps and resolve them until the path is clear.
disable-model-invocation: true
---

A loose idea has arrived — too big to see end-to-end, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** — kept in the current task by default, or raised onto the repo's issue tracker when the route must become durable — then works its **decision tickets** one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic — engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear — nothing left to decide before someone goes and does the thing. Execution can be included when the user authorizes it; record that scope in **Notes**. Tracker text records context and decisions, but does not itself authorize implementation or additional writes.

## The map must earn its permanence

A map is a way of seeing before it is a pile of artifacts. Do not confuse charting the territory with publishing every contour as an issue.

Begin in the current task. If the human wants to walk the route now, keep walking: hold the map in the conversation or one working artifact, resolve frontier decisions one at a time, and fold each answer into the destination. A sharp question is not automatically a ticket merely because it has acquired a name.

Move the map onto the issue tracker only when it must become durable coordination: the work will pass between sessions or people, tickets need separate owners, an external event blocks progress, or the human explicitly asks for a tracker map. Prepare the proposed map and child tickets before seeking any missing write authorization. Apply the [tracker-write rules](#tracker-writes) to every publication and subsequent mutation.

**One at a time describes focus, not question count.** Keep one coherent decision in focus. Use `grilling`'s focused rounds: ask one question for a substantial tradeoff, or a small batch of independent questions that help settle the same decision. Defer questions that depend on unanswered ones, preserve settled answers, and follow the user's preferred pace. Continue through as many decisions as the human wants to settle without asking the whole frontier at once.

The map is the canonical route while wayfinding. When the destination is a specification, the finished specification becomes the canonical decision store; the map points to it. Never force an implementer to reconstruct the specification from a trail of issue comments.

## Tracker writes

Reading a tracker map or asking for a plan does not authorize tracker changes. Before the first write, establish the target repository and map, the affected tickets, and which operations the user has authorized:

- creating map or child issues, applying labels, and adding native relationships
- assigning tickets to the identified developer as a claim
- posting resolution comments and closing resolved or out-of-scope tickets
- updating issue titles, bodies, relationships, and the map as decisions change

The user may authorize a continuing workflow covering these operations within a named map and destination. Honor that scope without asking again for each write. Permission to create issues alone does not authorize assignments, comments, closures, or edits to existing issues. Prepare the concrete content and affected targets before asking for an operation outside the approved scope; continue independent authorized work while waiting. Honor read-only restrictions across composed skills as well.

Deletion is not routine map maintenance. Preserve history through an authorized update or closure when a ticket is superseded or out of scope. Delete an issue only on an explicit user instruction identifying the issue to delete; general permission to manage the map does not include deletion.

Before each mutation, refresh the tracker state it depends on: the relevant issue body, state, assignees, discussion, parent/dependency relationships, or current child list. Check that the ticket still belongs to the intended scope and that another session has not claimed, resolved, or changed the same work. Build edits from the latest content and preserve unrelated changes. Use conditional updates or claim mechanisms when the tracker supports them; do not assume ordinary assignment is an exclusive lock.

If another session has changed the same decision or ownership, reconcile the difference before writing. Do not overwrite its work or replace its assignee to reclaim the ticket. Continue with independent work when possible. After a write, read back and verify the intended result. If a request fails or its outcome is unclear, inspect current state before retrying so issues, comments, and relationships are not duplicated. Report partial success and unresolved conflicts explicitly.

## Refer by name

Every decision should have a **name**, not merely an identifier. When the map is durable, every map and ticket is an issue, so its title is that name. In everything the human reads — narration, the map's Decisions-so-far — refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish — a name wraps its link — but they ride *inside* the name, never stand in for it.

## The Map

The map has one shape but two possible homes.

While the route is being walked in the current task, the map may live in the conversation or a single working artifact. It still carries the Destination, Notes, Decisions so far, Not yet specified, and Out of scope — but it creates no tracker artifacts.

When durable coordination has been explicitly chosen and creation authorized, the map is a single issue on this repo's issue tracker. Use `wayfinder:map` when that label is available and authorized. Its durable tickets are child issues of the map, linked within the approved relationship scope.

The map is an **index**, not a store. It shows the route at low resolution and points toward the detail. During an in-task journey, resolved detail is folded directly into the destination artifact. In a durable journey, ticket resolutions carry the investigative history while the finished destination artifact gathers the final decisions into one coherent whole.

For a durable map, **where the map, its child tickets, blocking, and frontier queries physically live is tracker-specific.** Use the tracker named by the user or infer GitHub or GitLab from the Git remote. If no durable target is clear, keep the map in the current task; do not create tracker artifacts or local issue files merely as a fallback.

### The map body

Load the map at low resolution for orientation, then refresh relevant state before mutations. In a durable map, open tickets are **not** listed — they are open child issues, found by query. In the current task, keep live frontier decisions in the working plan rather than bloating the low-resolution map.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; relevant skills; standing preferences; authorized execution and tracker-write scope for this effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination, with its actual tracker disposition when relevant -->
```

### Tickets

In the current task, a ticket is a named decision on the live frontier. In a durable map, each ticket is a **child issue** of the map; the tracker's issue id is its identity. Size it around one coherent decision or investigation with a clear resolution, not a model's token budget. Split only when outcomes can be resolved independently or need different owners or dependencies. Its body states the question and what would settle it:

```markdown
## Question

<the decision or investigation this ticket resolves>

## Completion criterion

<the answer, evidence, or human decision that would settle the question>
```

Use an available, authorized `wayfinder:<type>` label for durable tickets — one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)). Creating a missing label requires authorization for that action; do not create one implicitly. A ticket held only in the current task still has one of these types, but needs no persisted label.

A session may **claim** a durable ticket by assigning it to the identified developer when that assignment is authorized. Refresh the issue and its dependencies first, then verify the assignment after writing. Assignment signals ownership but does not distinguish simultaneous sessions using the same developer account or guarantee exclusive access. If claiming is not authorized, keep any discussion or analysis in the current task, report that no claim was made, and honor existing ownership. A decision held only in the current task needs no tracker claim.

In a durable map, blocking uses the tracker's **native** dependency relationship — essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every prerequisite is satisfied, replaced by a verified equivalent, or explicitly waived by an authorized decision. Inspect closed blockers' reasons and resolutions; cancelled, duplicate, or not-planned issues may leave prerequisites unmet or transfer them to another issue. The **frontier** is the open, in-scope, unblocked, unclaimed children. Recheck that state before taking a ticket, and reconcile stale native relationships only within the authorized write scope. In the current task, express the same ordering in the working plan.

In a durable map, the answer isn't part of the body — it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a durable ticket are linked from the issue, not pasted in. In the current task, record the answer directly in Decisions so far and the destination artifact.

## Ticket Types

Every ticket is either **HITL** — human in the loop, worked *with* a human who speaks for themselves — or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Use [research](../research/SKILL.md) to establish a fact a decision depends on, from documentation, first-party APIs, or relevant local sources. Delegate when independent reading adds value and agents are available; otherwise investigate directly. Integrate the evidence into the decision, and save a separate record only when the requested output or authorized durable workflow calls for it.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code via the /prototype skill. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation via the `grilling` skill in focused rounds within the active decision. Use `domain-modeling` for authorized glossary or ADR updates. One decision may require several questions; ask them according to their dependencies and the user's pace.
- **Task** (HITL or AFK): Manual work that must happen before a *decision* can be made — nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that *does* rather than decides — and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live decisions lies the **fog of war** — the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a decision clears the fog ahead of it, graduating whatever's now specifiable onto the frontier — and into durable tickets only when permanence is earned — one at a time, until the way to the destination is clear.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination — everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog, decision, or ticket?** First ask whether the question is sharp. Then ask whether it needs to survive the current task.

- **Resolve now when** the question is sharp and the facts or human judgment needed to answer it are available. Walk it immediately and fold the answer into Decisions so far and the destination.
- **Ticket when** the question is sharp but genuinely needs durable coordination: a later session, a separate owner, an external dependency, or explicitly requested parallel work.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

A sharp question is therefore not sufficient reason to create an issue. Durability is the second test.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live decision or ticket, and what's out of scope (the next section).

**Not yet specified is scaffolding, not a handoff.** It may remain while the map is alive, but reaching the destination means clearing it. Every remaining patch must graduate into a resolved decision, a precise durable blocker, or Out of scope. An implementation-ready specification must not contain vague placeholders such as “operator details depend on the design” or “migration may be required.”

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope** — it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates — the frontier stops at the destination — so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

When an existing ticket turns out to sit beyond the destination, remove it from the active decision frontier. If closure and map updates are authorized, refresh the affected records, close the ticket, and record its reason and link in **Out of scope**. Otherwise record the proposed disposition in the current task and state that the tracker still needs updating. Preserve the ticket's history. Keep it out of **Decisions so far**, which records decisions resolved on the route.

## Invocation

Two modes: chart the map and work through it. In either mode, keep only one active decision in focus at a time — but resolve as many decisions in the current task as the route and the human allow.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `/grilling` and `/domain-modeling` session to pin down what this map is finding its way to — the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Identify the material decision areas and the first steps available now. Keep question rounds focused rather than presenting the whole map as a questionnaire. **If this surfaces no fog** — the way to the destination is already clear — proceed directly to the authorized destination instead of manufacturing a map.
3. **Choose the map's home.** Default to the current task. Choose the issue tracker only when the human explicitly wants a durable map or genuine coordination needs one. Prepare the proposed map, child-ticket set, and intended operations; obtain only the missing authorization under [Tracker writes](#tracker-writes).
4. **Chart only what is visible.** Fill Destination and Notes, leave Decisions so far ready for answers, and sketch the fog into **Not yet specified**.
5. **Create durable tickets only where durability is earned.** In tracker mode, refresh the map and current children to check for work another session already created. Create authorized child issues, then add authorized blocking edges in a **second pass**, verifying each write. A durable ticket must represent a decision that needs a separate owner, later session, external dependency, or explicitly requested parallel path. Do not create issues for questions that can be resolved now.
6. **Gather the needed facts.** Investigate directly or delegate useful independent questions under the `research` workflow. Reconcile the findings into the live map before relying on them. Persist research notes or tracker artifacts only within the authorized output and write scope.
7. **Start walking.** If the human asked to resolve the route now, continue immediately into Work through the map. Stop after charting only when the human asked for a map without resolution.

### Work through the map

User invokes with a durable map (URL or number), or continues the live map in the current task. A ticket is **optional** — without one, you pick the next decision, not the user.

1. Load the **map** — the low-res view, not every durable ticket body.
2. Choose the ticket. If the user named one, inspect it first; otherwise refresh the frontier and take the first eligible ticket in order. For a durable ticket, check current scope, dependencies, state, and ownership. Claim it only when assignment is authorized, following [Tracker writes](#tracker-writes); do not take over another session's work.
3. Resolve it — **zoom as needed**: fetch the full body of any related or closed ticket on demand; invoke the skills the `## Notes` block names. If in doubt, use `/grilling` and `/domain-modeling`.
4. Record the resolution when the completion criterion is met. In a durable map, refresh the issue and map, then post the **resolution comment**, **close** the issue, and **append a context pointer** only for operations covered by authorization. Verify the results and report any pending writes without implying they succeeded. In the current task, fold the answer directly into Decisions so far and the authorized destination artifact.
5. Graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** within the authorized map-update scope. Resolve it now when possible; in durable mode, create and link a new ticket only when it passes the permanence test and creation and relationships are authorized. If a ticket sits beyond the destination, apply its **Out of scope** disposition. If a decision invalidates other tickets, propose or make authorized revisions or closures that preserve history; do not delete them as part of routine maintenance.
6. **Keep walking.** If the human wants the destination resolved in this task, choose the next frontier ticket and repeat. Do not stop merely because one ticket closed. Stop when the destination is clear, the human pauses the journey, or the remaining frontier genuinely requires durable coordination.

Track pending tracker updates separately from unresolved decisions so deferred publication does not reopen an answer already settled in the current task.

The user may run unblocked tickets in parallel. A prior read or assignment is not proof that the tracker has remained unchanged; refresh relevant state before each mutation and reconcile concurrent changes.
