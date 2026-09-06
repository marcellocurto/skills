# Icons

Use the project's configured `iconLibrary` or established imports unless the user requests a change. Check project context rather than assuming `lucide-react`. Placement and sizing below are defaults for components that support them; the installed API and requested design govern customization.

---

## Icons in Button use data-icon attribute

Use `data-icon="inline-start"` (prefix) or `data-icon="inline-end"` (suffix) when the installed Button supports that convention. Prefer its built-in sizing before adding local overrides.

**Less suitable default:**

```tsx
<Button>
  <SearchIcon className="mr-2 size-4" />
  Search
</Button>
```

**Preferred default:**

```tsx
<Button>
  <SearchIcon data-icon="inline-start"/>
  Search
</Button>

<Button>
  Next
  <ArrowRightIcon data-icon="inline-end"/>
</Button>
```

---

## Prefer component-owned icon sizing

Inspect the component's CSS before specifying icon size. Use its default when it fits; add a scoped override when the requested design or existing convention needs another size, and verify alignment and control dimensions.

**Less suitable default:**

```tsx
<Button>
  <SearchIcon className="size-4" data-icon="inline-start" />
  Search
</Button>

<DropdownMenuItem>
  <SettingsIcon className="mr-2 size-4" />
  Settings
</DropdownMenuItem>
```

**Preferred default:**

```tsx
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

<DropdownMenuItem>
  <SettingsIcon />
  Settings
</DropdownMenuItem>
```

---

## Pass icons as component objects, not string keys

Prefer `icon={CheckIcon}` for component composition. Preserve identifier-based APIs when an existing data or serialization contract requires them; do not add lookup machinery solely to pass a component indirectly.

**Less suitable default:**

```tsx
const iconMap = {
  check: CheckIcon,
  alert: AlertIcon,
}

function StatusBadge({ icon }: { icon: string }) {
  const Icon = iconMap[icon]
  return <Icon />
}

<StatusBadge icon="check" />
```

**Preferred default:**

```tsx
// Import from the project's configured iconLibrary (e.g. lucide-react, @tabler/icons-react).
import { CheckIcon } from "lucide-react"

function StatusBadge({ icon: Icon }: { icon: React.ComponentType }) {
  return <Icon />
}

<StatusBadge icon={CheckIcon} />
```
