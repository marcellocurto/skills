---
title: Cache Property Access in Loops
impact: LOW-MEDIUM
impactDescription: reduces lookups
tags: javascript, loops, optimization, caching
---

## Cache Property Access in Loops

Consider hoisting repeated property reads only on a demonstrated hot path when the values stay invariant during the loop. Getters, proxies, or mutation by the loop body may make repeated reads observable. Preserve that behavior and skip the rewrite when the measured or expected saving does not justify the added local state.

**Incorrect (3 lookups × N iterations):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct (1 lookup total):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```
