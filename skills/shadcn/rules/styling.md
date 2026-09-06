# Styling & Customization

See [customization.md](../customization.md) for theming, CSS variables, and adding custom colors.

These are styling defaults, not API or accessibility requirements. Follow the requested design and established project conventions when they justify another approach. Compare examples for fit with those defaults; do not rewrite valid existing styles solely to match them.

## Contents

- Semantic colors
- Built-in variants first
- className for layout and local styling
- Prefer gap for flex and grid layouts
- Prefer size-* over w-* h-* when equal
- Prefer truncate shorthand
- Prefer semantic theme colors
- Use cn() for conditional classes
- Inspect overlay stacking before overriding it
- Reuse available shimmer and scroll-fade utilities

---

## Semantic colors

**Less suitable default:**

```tsx
<div className="bg-blue-500 text-white">
  <p className="text-gray-600">Secondary text</p>
</div>
```

**Preferred default:**

```tsx
<div className="bg-primary text-primary-foreground">
  <p className="text-muted-foreground">Secondary text</p>
</div>
```

---

## Prefer semantic status colors

For positive, negative, or status indicators, prefer existing Badge variants, semantic tokens like `text-destructive`, or the project's custom CSS variables. Match established meaning and contrast; a direct color value may be appropriate for an explicitly requested design or existing convention.

**Less suitable default:**

```tsx
<span className="text-emerald-600">+20.1%</span>
<span className="text-green-500">Active</span>
<span className="text-red-600">-3.2%</span>
```

**Preferred default:**

```tsx
<Badge variant="secondary">+20.1%</Badge>
<Badge>Active</Badge>
<span className="text-destructive">-3.2%</span>
```

If a needed semantic color is missing, inspect existing theme conventions and make a scoped token addition when the task authorizes it. Ask only if the choice changes product meaning or exceeds the requested design scope (see [customization.md](../customization.md)).

---

## Built-in variants first

**Less suitable default:**

```tsx
<Button className="border border-input bg-transparent hover:bg-accent">
  Click me
</Button>
```

**Preferred default:**

```tsx
<Button variant="outline">Click me</Button>
```

---

## className for layout and local styling

Use `className` for layout and justified local styling. Prefer existing variants and tokens before overriding a component's colors or typography. A scoped override is appropriate when it expresses the requested design without breaking the component's behavior, contrast, or theme states.

**Less suitable default:**

```tsx
<Card className="bg-blue-100 text-blue-900 font-bold">
  <CardContent>Dashboard</CardContent>
</Card>
```

**Preferred default:**

```tsx
<Card className="max-w-md mx-auto">
  <CardContent>Dashboard</CardContent>
</Card>
```

To customize a component's appearance, prefer these approaches in order:
1. **Built-in variants** — `variant="outline"`, `variant="destructive"`, etc.
2. **Semantic color tokens** — `bg-primary`, `text-muted-foreground`.
3. **CSS variables** — define custom colors in the global CSS file (see [customization.md](../customization.md)).

---

## Prefer gap for flex and grid layouts

Prefer `gap-*` when the container uses flex or grid. Preserve an intentional block layout using `space-y-*` or `space-x-*`; changing display mode merely to replace a utility can change behavior.

```tsx
<div className="flex flex-col gap-4">
  <Input />
  <Input />
  <Button>Submit</Button>
</div>
```

---

## Prefer size-* over w-* h-* when equal

Prefer `size-10` over `w-10 h-10` when equal dimensions are intended. This shorthand alone does not justify rewriting existing classes.

---

## Prefer truncate shorthand

Prefer `truncate` when it expresses the intended single-line behavior. Preserve another combination when the layout needs different overflow or wrapping.

---

## Prefer semantic theme colors

Prefer semantic tokens such as `bg-background text-foreground` for shared light/dark roles. Explicit `dark:` overrides are appropriate when the requested treatment or project convention requires them; verify both themes.

---

## Use cn() for conditional classes

Prefer the project's `cn()` utility for conditional or merged class names. A simple existing expression is not a defect solely because it uses a ternary.

**Less suitable default:**

```tsx
<div className={`flex items-center ${isActive ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
```

**Preferred default:**

```tsx
import { cn } from "@/lib/utils"

<div className={cn("flex items-center", isActive ? "bg-primary text-primary-foreground" : "bg-muted")}>
```

---

## Inspect overlay stacking before overriding it

Overlay components usually own their stacking. Inspect the installed styles and portal behavior before adding a z-index override. Make one only for a demonstrated layering need and verify that related overlays and focus behavior still work.

---

## Reuse available shimmer and scroll-fade utilities

For a live "thinking…" or loading-text shimmer, prefer the existing `shimmer` utility when available and appropriate. Use a custom animation only when the requested effect or environment needs it.

For scroll-aware edge fading, prefer an available `scroll-fade` utility and its axis variants. Inspect the installed chat components before duplicating effects they already provide.

**Less suitable default:**

```tsx
<span className="animate-pulse bg-gradient-to-r from-muted-foreground/40 via-foreground/70 to-muted-foreground/40 bg-clip-text text-transparent [animation:shimmer_1.6s_infinite]">
  Thinking…
</span>
```

**Preferred default:**

```tsx
<span className="shimmer">Thinking…</span>
```
