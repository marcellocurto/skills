---
name: wayfinder
description: Plan a huge chunk of work — possibly more than one agent session can hold — as a shared map of decision tickets, and resolve them one at a time until the way to the destination is clear. Keep the map in the current task by default; publish it to an issue tracker only when the user wants durable coordination or the work genuinely requires separate owners, sessions, or external blockers.
disable-model-invocation: true
---

A loose idea has arrived — too big to see end-to-end, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** — kept in the current task by default, or raised onto the repo's issue tracker when the route must become durable — then works its **decision tickets** one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic — engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear — nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes** — carrying execution into the map itself — but absent that, produce decisions, not deliverables.

## The map must earn its permanence

A map is a way of seeing before it is a pile of artifacts. Do not confuse charting the territory with publishing every contour as an issue.

Begin in the current task. If the human wants to walk the route now, keep walking: hold the map in the conversation or one working artifact, resolve frontier decisions one at a time, and fold each answer into the destination. A sharp question is not automatically a ticket merely because it has acquired a name.

Move the map onto the issue tracker only when it must become durable coordination: the work will pass between sessions or people, tickets need separate owners, an external event blocks progress, or the human explicitly asks for a tracker map. Before writing to the tracker, show the proposed map and child tickets and get confirmation unless the human has already explicitly authorized issue creation.

**One at a time describes focus, not throughput.** Resolve one active decision at a time, but continue through as many frontier decisions as the human wants to settle in the current task.

The map is the canonical route while wayfinding. When the destination is a specification, the finished specification becomes the canonical decision store; the map points to it. Never force an implementer to reconstruct the specification from a trail of issue comments.

## Refer by name

Every decision should have a **name**, not merely an identifier. When the map is durable, every map and ticket is an issue, so its title is that name. In everything the human reads — narration, the map's Decisions-so-far — refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish — a name wraps its link — but they ride *inside* the name, never stand in for it.

## The Map

The map has one shape but two possible homes.

While the route is being walked in the current task, the map may live in the conversation or a single working artifact. It still carries the Destination, Notes, Decisions so far, Not yet specified, and Out of scope — but it creates no tracker artifacts.

When durable coordination has been explicitly chosen, the map is a single issue on this repo's issue tracker, labelled `wayfinder:map`. Its durable tickets are child issues of the map.

The map is an **index**, not a store. It shows the route at low resolution and points toward the detail. During an in-task journey, resolved detail is folded directly into the destination artifact. In a durable journey, ticket resolutions carry the investigative history while the finished destination artifact gathers the final decisions into one coherent whole.

**Where the map, its child tickets, blocking, and frontier queries physically live is tracker-specific.** The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if not. Consult the tracker doc's "Wayfinding operations" section for how _this_ repo expresses them. If no tracker has been provided, default to the local-markdown tracker.

### The map body

The whole map at low resolution, loaded once per session. In a durable map, open tickets are **not** listed — they are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

In the current task, a ticket is a named decision on the live frontier. In a durable map, each ticket is a **child issue** of the map; the tracker's issue id is its identity. Its body is the question, sized to one 100K token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label — one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)).

A session **claims** a durable ticket by assigning it to the dev driving the map, **first**, before any work, so concurrent sessions skip it. That assignee _is_ the claim: an open, unassigned ticket is unclaimed. A ticket held only in the current task needs no tracker claim.

Blocking uses the tracker's **native** dependency relationship — essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children — the edge of the known.

In a durable map, the answer isn't part of the body — it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a durable ticket are linked from the issue, not pasted in. In the current task, record the answer directly in Decisions so far and the destination artifact.

## Ticket Types

Every ticket is either **HITL** — human in the loop, worked *with* a human who speaks for themselves — or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a `/research` **subagent**. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code via the /prototype skill. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation via the /grilling and /domain-modeling skills, one question at a time. The default case.
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

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination — mis-scoped in while charting, or exposed by a resolution — **close it** (a closed ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It stays out of **Decisions so far**, which records the route actually walked — a scope boundary isn't a step on it.

## Invocation

Two modes: chart the map and work through it. In either mode, keep only one active decision in focus at a time — but resolve as many decisions in the current task as the route and the human allow.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `/grilling` and `/domain-modeling` session to pin down what this map is finding its way to — the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** — the way to the destination is already clear — proceed directly to the destination instead of manufacturing a map.
3. **Choose the map's home.** Default to the current task. Choose the issue tracker only when the human explicitly wants a durable map or genuine coordination needs one. Before creating tracker artifacts, show the proposed map and child-ticket set.
4. **Chart only what is visible.** Fill Destination and Notes, leave Decisions so far ready for answers, and sketch the fog into **Not yet specified**.
5. **Create durable tickets only where durability is earned.** In tracker mode, create those child issues, then wire blocking edges in a **second pass**. A durable ticket must represent a decision that needs a separate owner, later session, external dependency, or explicitly requested parallel path. Do not create issues for questions that can be resolved now.
6. **Fire the research subagents.** Let them scout ahead and return findings to the live map. Create branches or tracker artifacts for their work only when the durable map explicitly calls for them and repository authority allows it.
7. **Start walking.** If the human asked to resolve the route now, continue immediately into Work through the map. Stop after charting only when the human asked for a map without resolution.

### Work through the map

User invokes with a durable map (URL or number), or continues the live map in the current task. A ticket is **optional** — without one, you pick the next decision, not the user.

1. Load the **map** — the low-res view, not every durable ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. For a durable ticket, **claim it**: assign it to yourself before any work.
3. Resolve it — **zoom as needed**: fetch the full body of any related or closed ticket on demand; invoke the skills the `## Notes` block names. If in doubt, use `/grilling` and `/domain-modeling`.
4. Record the resolution. In a durable map, post the answer as a **resolution comment**, **close** the issue, and **append a context pointer** to the map's Decisions so far. In the current task, fold the answer directly into Decisions so far and the destination artifact.
5. Graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified**. Resolve it now when possible; in durable mode, create-then-wire a new ticket only when it passes the permanence test. If the answer reveals a ticket — this one or another — sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.
6. **Keep walking.** If the human wants the destination resolved in this task, choose the next frontier ticket and repeat. Do not stop merely because one ticket closed. Stop when the destination is clear, the human pauses the journey, or the remaining frontier genuinely requires durable coordination.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
