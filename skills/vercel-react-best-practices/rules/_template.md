---
title: Rule Title Here
impact: MEDIUM
impactDescription: Describe the avoidable cost and the conditions where it matters
tags: tag1, tag2
---

## Rule Title Here

**Impact: MEDIUM (optional impact description)**

Explain the concrete mechanism, workload, and evidence that make this rule applicable. State when the existing approach is adequate and which contracts an optimization must preserve. Present library or cache additions as conditional options.

Use qualitative impact descriptions by default. A numerical result needs its source and workload; label illustrative estimates explicitly and never present them as measurements of the reader's application.

**Incorrect (description of what's wrong):**

```typescript
// Bad code example here
const bad = example()
```

**Correct (description of what's right):**

```typescript
// Good code example here
const good = example()
```

Reference: [Link to documentation or resource](https://example.com)
