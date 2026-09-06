---
title: Per-Request Deduplication with React.cache()
impact: MEDIUM
impactDescription: deduplicates within request
tags: server, cache, react-cache, deduplication
---

## Per-Request Deduplication with React.cache()

Consider `React.cache()` when the same costly computation or read repeats during a React Server Component render and sharing its result within that request preserves behavior. Reuse existing deduplication first. It is not a general-purpose server cache or a reason to cache every authentication check or database query.

**Usage:**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

During a supported server render, calls to the same memoized function can share the result. React invalidates this cache between server requests, and errors are cached too. Verify that those semantics fit the operation.

**Avoid inline objects as arguments:**

`React.cache()` uses shallow equality (`Object.is`) to determine cache hits. Inline objects create new references each call, preventing cache hits.

**Incorrect (always cache miss):**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// Each call creates new object, never hits cache
getUser({ uid: 1 })
getUser({ uid: 1 })  // Cache miss, runs query again
```

**Correct (cache hit):**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({ where: { id: uid } })
})

// Primitive args use value equality
getUser(1)
getUser(1)  // Cache hit, returns cached result
```

If you must pass objects, pass the same reference:

```typescript
const params = { uid: 1 }
getUser(params)  // Query runs
getUser(params)  // Cache hit (same reference)
```

**Next.js-Specific Note:**

Check the installed Next.js version and execution context for existing request memoization before adding another layer. Consider `React.cache()` for repeated non-fetch work only when its request scope and result/error reuse fit the requirement. A single call or an already-deduplicated operation gains nothing merely from another wrapper.

Reference: [React.cache documentation](https://react.dev/reference/react/cache)
