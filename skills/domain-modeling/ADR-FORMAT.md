# ADR Format

An ADR records a decision the system follows today and the reason for it. Every ADR in the directory should be true of the current system, so a reader can act on it without first checking whether it still applies.

## Location and numbering

Follow the project's ADR directory, file naming, and numbering. When no convention exists, use `docs/adr/` with sequential names such as `0001-slug.md` and `0002-slug.md`. Create the fallback directory only when a qualifying decision is settled and documentation writes are authorized. In discussion mode, keep the proposed ADR in the response without creating files.

When names are numbered, take the next unused number from the actual ADR directory; do not start another sequence in `docs/adr/` merely because records live elsewhere. Never renumber existing ADRs. Gaps left by deleted ADRs are expected.

## Shape

Write every new or rewritten ADR in this shape unless the project's instructions or an ADR README document a different format. The style of existing ADRs is not a documented format, so do not copy the length or sections of older records.

```md
# {The decision, stated as a sentence}

{What we decided and why. When an outside constraint ruled out the obvious option, name the constraint in the first sentence.}

{Optional: We rejected {alternative} because {reason}.}

{Optional: consequences a reader would not guess from the decision.}
```

Write as much as the decision needs to be understood and no more. Most ADRs are a single paragraph. Add the rejected alternative only when someone would otherwise propose it again, and consequences only when they would surprise a reader.

Naming the outside constraint first, as in "Because database documents are capped at 1 MiB, …", lets a later change that removes the constraint find every ADR that depends on it.

Example:

```md
# Blob deletes are queued with the row and retried until storage confirms

Deleting a row that names a blob queues the blob's key in the same transaction, and a background loop retries the delete until storage confirms it. We rejected deleting the blob right after the row: if that single attempt failed, nothing would still know the key, and the blob would stay in storage for good.
```

## Leave out

These details describe history or implementation, and they become false or irrelevant long before the decision changes:

- issue, pull request, and commit references that narrate history, such as "since #529"; a link to evidence that supports the reason, such as an incident report or a benchmark, may stay
- how the system behaved before the decision, including phrases such as "before this" or "previously"
- migration, backfill, and rollout steps
- file paths and the names of tables, fields, functions, and jobs; name the concept instead, such as "the chunk table", so a rename does not make the ADR wrong
- anything a code comment, schema, or type already states
- mechanism the decision does not depend on

## Group decisions that change together

Before writing an ADR, look for one that already records the same decision, and update it instead of creating another file. Put two decisions in one ADR only when understanding or revising one requires the other. A decision that can be revised on its own keeps its own ADR, even when it shares a subject with others. The title of a combined ADR still states what was decided, not the subsystem it applies to.

## What qualifies

[SKILL.md](SKILL.md) states the three criteria a decision must meet. Decisions that typically meet them:

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library: just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it; otherwise someone will suggest GraphQL again in six months.
