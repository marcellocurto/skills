---
title: Prevent Waterfall Chains in API Routes
impact: CRITICAL
impactDescription: overlaps independent work when sequencing is unnecessary
tags: api-routes, server-actions, waterfalls, parallelization
---

## Prevent Waterfall Chains in API Routes

When a route's critical path contains avoidable sequential waits, start genuinely independent operations together. Do not move authorized work before its authorization check, or change ordering, failure, or resource-use semantics merely to overlap requests.

**Incorrect (config waits for auth, data waits for both):**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**Correct (auth and config start immediately):**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  // Both promises get a handler in the same tick they are created. Awaiting
  // `sessionPromise` on its own first would leave `configPromise` unobserved;
  // a fast config failure would then be an unhandled rejection.
  const [config, data] = await Promise.all([
    configPromise,
    sessionPromise.then(session => fetchData(session.user.id))
  ])
  return Response.json({ data, config })
}
```

Attach a handler to every promise you start before the first `await`, by passing it to `Promise.all` or chaining `.then` immediately. A promise left unobserved across an `await` becomes an unhandled rejection if it fails first, which crashes a Node process by default.

For more complex dependency chains, compare existing scheduling facilities and direct promise composition before considering `better-all`. See [Dependency-Based Parallelization](./async-dependencies.md) for the conditions that justify it.
