# Type Design

Use this guidance when a statically typed module's state, function signatures, variants, or external data shape carry correctness-critical invariants. The goal is not maximum precision. Use the type system to eliminate realistic failures while keeping interfaces usable and functions as total as their behavior allows.

## Encode the Necessary Invariants

- **Make illegal states unrepresentable.** Prefer explicit variants over bags of optional fields or booleans that can contradict one another. Require a real invariant; do not introduce a sum type when every combination is valid and easy to understand.
- **Construct the valid shape directly.** When code repeatedly checks a condition before an operation can succeed, ask whether a representation can make the condition structural. A non-empty sequence can be a head plus the remainder; an ordered interval may be a start plus a duration rather than two independently mutable endpoints.
- **Distinguish semantic primitives when confusion is plausible.** Brand or wrap equal-shaped values such as different identifier kinds when callers can realistically mix them up. Validate at construction and trust the type afterward. Skip the wrapper when it adds ceremony without preventing a credible mistake.
- **Handle variants exhaustively.** Use the language's exhaustive matching mechanism so a new variant points to every place that needs a decision. A default branch that silently accepts future cases defeats this protection.

## Treat External Data as Untrusted

Parse RPC payloads, JSON, configuration, environment variables, database rows, and other external values at the system edge before they enter the typed model. Inside the module, accept the parsed type rather than repeating validation or carrying `unknown` through the implementation.

When an OpenAPI document, protocol definition, database schema, or other artifact truly owns an external contract, derive its transport type rather than hand-maintaining a duplicate. Keep transport and storage representations behind the seam: parse or map them into domain types when the domain owns different names, invariants, or behavior.

## Treat Escape Hatches as Evidence

Trace `any`, casts, unsafe coercions, non-null assertions, and assertion helpers to the fact they claim is true:

- Prove the fact through parsing, narrowing, construction, or a stronger upstream contract when practical.
- Keep an unavoidable interop cast narrow and adjacent to the evidence that justifies it.
- Do not spread an asserted type through the module and mistake compiler silence for proof.

An escape hatch is not automatically a bug. It is an explicit proof obligation and a useful signal that the system edge or model may be too weak.

## Stop When Partiality Is Gone

Strengthen a type where an operation otherwise has no valid answer or must throw for a representable input. Do not strengthen it merely to describe data more precisely. Extra precision costs reuse, inference quality, conversions, and caller ceremony.

Ask:

- Which invalid state or mismatched value becomes impossible?
- Which runtime check, assertion, or failure disappears?
- Will adding a new variant force every necessary decision?
- Is this type derived from the artifact that actually owns the contract?
- Does the added precision buy safety at the callers that use it?

If those answers reveal no concrete benefit, keep the simpler type.
