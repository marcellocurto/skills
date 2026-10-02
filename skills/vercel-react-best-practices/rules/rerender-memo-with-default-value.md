---

title: Extract Default Non-primitive Parameter Value from Memoized Component to Constant
impact: MEDIUM
impactDescription: restores memoization by using a constant for default value
tags: rerender, memo, optimization

---

## Extract Default Non-primitive Parameter Value from Memoized Component to Constant

A default value for a non-primitive optional parameter, such as an array, function, or object, is re-created on every render of the component. `memo()` itself is unaffected, because defaults are applied after props are compared, but any memoized child, `useMemo`, `useCallback`, or effect that receives the default sees a new identity each render and re-runs.

To address this issue, extract the default value into a constant.

**Incorrect (`onClick` is a new function on every render of `UserAvatar`):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**Correct (stable default value):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```
