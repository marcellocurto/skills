---
title: Dependency-Based Parallelization
impact: CRITICAL
impactDescription: avoids waiting on unrelated dependencies; gains depend on task durations
tags: async, parallelization, dependencies, better-all
---

## Dependency-Based Parallelization

Use this pattern when an operation waits for work it does not depend on and that wait matters on the actual path. Express the dependency graph with existing scheduling facilities or ordinary promises first. Preserve required sequencing, error handling, and cancellation behavior.

**Incorrect (profile waits for config unnecessarily):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**Direct dependency scheduling:**

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

**Optional library for a sufficiently complex graph:**

Consider `better-all` when it is already used by the project or its dependency scheduling materially simplifies the demonstrated workload. Do not add it for a small graph that is already clear with promises.

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

Reference: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)
