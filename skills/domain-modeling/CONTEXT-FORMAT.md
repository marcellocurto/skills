# CONTEXT.md Format

Use this as a fallback glossary format when the project has no established convention. Follow existing locations and document structure first. Create or edit records only in the working mode authorized under [SKILL.md](SKILL.md#choose-the-working-mode).

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: {Words that obscure a material distinction in this context, if any}

**Invoice**:
A request for payment sent to a customer after delivery.

**Customer**:
A person or organization that places orders.
```

## Rules

- **Use established domain names.** Record the agreed canonical term. Use `_Avoid_` only for wording that confuses distinct concepts or changes meaning, not every harmless synonym.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

When no existing documentation convention governs, a single context can use one `CONTEXT.md` at the repo root.

For multiple contexts without an existing map, a `CONTEXT-MAP.md` can list where each context's glossary lives and how they relate. Use it only when the distinctions need a map; do not create one merely because the repository has multiple packages.

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md): receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

Choose the structure from the project's existing documentation and domain ownership:

- Follow the current context map and glossary links, even when their names differ from these examples.
- A root `CONTEXT.md` may serve several purposes and does not establish that there is only one domain context. Preserve its unrelated sections.
- Only when no suitable glossary or convention exists, create the fallback glossary lazily after a term is resolved and writing is authorized.

Infer the relevant context from the topic and existing ownership. Ask only when ambiguity would materially change the definition or where it belongs.
