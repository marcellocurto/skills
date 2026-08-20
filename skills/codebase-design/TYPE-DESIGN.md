# Type Design

Use this guidance when a module's types carry correctness-critical rules. Encode only the rules that prevent a realistic failure; extra precision makes interfaces harder to use.

## Rules

- Represent mutually exclusive cases as explicit variants instead of fields that can contradict one another. Do this only when some combinations are genuinely invalid.
- Give equal-shaped values distinct types when callers can realistically confuse them. Skip wrappers that prevent no credible mistake.
- Parse external input once at the system edge. Modules should receive validated values rather than repeat checks or carry `unknown` through their implementation.
- Generate transport types when a schema owns the external contract. Map them into domain types when storage or wire names do not express the domain's rules.
- Match variants exhaustively so adding a case exposes every decision that must change. Avoid fallback branches that silently absorb future cases.
- Treat `any`, casts, unsafe coercions, and non-null assertions as claims that need evidence. Prove the claim through validation or narrowing, or isolate an unavoidable interop cast beside its justification.

## Precision Check

Add type precision only when it removes a runtime failure, repeated check, or realistic value mix-up. Ask:

- What bad value or combination becomes impossible?
- Which check, assertion, or failure disappears?
- Will a new variant force the necessary callers to decide what it means?
- Does the referenced schema actually own this contract?
- Is the safety gain worth the conversion and caller cost?

If the answers reveal no concrete benefit, keep the simpler type.
