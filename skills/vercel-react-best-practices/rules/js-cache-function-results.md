---
title: Cache Repeated Function Calls
impact: MEDIUM
impactDescription: avoids costly repeated computation under a suitable cache policy
tags: javascript, cache, memoization, performance
---

## Cache Repeated Function Calls

Cache a computation only when repeated inputs create meaningful work and returning a prior result preserves the contract. Prefer an existing cache or reuse within the current operation before adding shared state. Cheap or infrequent computation may be clearer and faster without cache bookkeeping.

Choose keys that include every input affecting the result. Establish cache ownership, lifetime, memory bounds, and invalidation. Module scope is appropriate only when sharing across those callers is intended; it is not the default merely because a Map can be accessed anywhere.

**Example: reuse an expensive calculation within one render:**

```tsx
function ProjectList({ projects }: { projects: Project[] }) {
  const slugs = new Map<string, string>()

  return (
    <div>
      {projects.map(project => {
        let slug = slugs.get(project.name)
        if (slug === undefined) {
          slug = slugify(project.name)
          slugs.set(project.name, slug)
        }
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

This example is useful only if repeated names and the computation's cost justify the Map. Entries expire with the render rather than accumulating across the process. For reuse across renders or requests, evaluate the relevant framework facility and its lifetime before choosing a broader cache.

Do not cache authentication state or mutable external data using this pure-computation pattern. Their changing inputs and freshness requirements need an explicit owner and invalidation policy.
