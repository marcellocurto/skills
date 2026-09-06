# Component Composition

Required nesting and props depend on the installed component and primitive library. Preserve those contracts and accessibility behavior. Card sections, grouping wrappers, and reuse of presentation components are defaults; adapt them to the requested design and established project patterns.

## Contents

- Group items where the API or content requires it
- Callouts use Alert
- Empty states use Empty component
- Toast notifications follow the project base
- Choosing between overlay components
- Dialog, Sheet, and Drawer always need a Title
- Card structure
- Loading behavior follows the installed Button API
- TabsTrigger must be inside TabsList
- Provide an appropriate avatar fallback
- Use Separator instead of raw hr or border divs
- Use Skeleton for loading placeholders
- Use Badge instead of custom styled spans

---

## Group items where the API or content requires it

Use grouping components when the installed API requires them or when related items need a shared label or grouping. The examples and table show common pairings, not a universal requirement to wrap every item in every base.

**Ungrouped items:**

```tsx
<SelectContent>
  <SelectItem value="apple">Apple</SelectItem>
  <SelectItem value="banana">Banana</SelectItem>
</SelectContent>
```

**Grouped items:**

```tsx
<SelectContent>
  <SelectGroup>
    <SelectItem value="apple">Apple</SelectItem>
    <SelectItem value="banana">Banana</SelectItem>
  </SelectGroup>
</SelectContent>
```

Common item/group pairings:

| Item | Group |
|------|-------|
| `SelectItem`, `SelectLabel` | `SelectGroup` |
| `DropdownMenuItem`, `DropdownMenuLabel`, `DropdownMenuSub` | `DropdownMenuGroup` |
| `MenubarItem` | `MenubarGroup` |
| `ContextMenuItem` | `ContextMenuGroup` |
| `CommandItem` | `CommandGroup` |
| `MessageScrollerItem` | `MessageScrollerContent` |
| `Message` (consecutive, same sender) | `MessageGroup` |
| `Bubble` (stacked) | `BubbleGroup` |
| `Attachment` (in a row) | `AttachmentGroup` |

Chat components nest in a fixed order (`MessageScrollerProvider` → `MessageScroller` → `MessageScrollerViewport` → `MessageScrollerContent` → `MessageScrollerItem`). See [chat.md](./chat.md).

---

## Callouts use Alert

```tsx
<Alert>
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>Something needs attention.</AlertDescription>
</Alert>
```

---

## Empty states use Empty component

```tsx
<Empty>
  <EmptyHeader>
    <EmptyMedia variant="icon"><FolderIcon /></EmptyMedia>
    <EmptyTitle>No projects yet</EmptyTitle>
    <EmptyDescription>Get started by creating a new project.</EmptyDescription>
  </EmptyHeader>
  <EmptyContent>
    <Button>Create Project</Button>
  </EmptyContent>
</Empty>
```

---

## Toast notifications follow the project base

Preserve the project's established toast implementation. For a Base UI project using the `toast` component:

```tsx
import { toast } from "@/components/ui/toast"

toast.add({
  title: "Changes saved.",
})
```

For a Radix or React Aria project using Sonner:

```tsx
import { toast } from "sonner"

toast.success("Changes saved.")
toast.error("Something went wrong.")
toast("File deleted.", {
  action: { label: "Undo", onClick: () => undoDelete() },
})
```

---

## Choosing between overlay components

| Use case | Component |
|----------|-----------|
| Focused task that requires input | `Dialog` |
| Destructive action confirmation | `AlertDialog` |
| Side panel with details or filters | `Sheet` |
| Mobile-first bottom panel | `Drawer` |
| Quick info on hover | `HoverCard` |
| Small contextual content on click | `Popover` |

---

## Dialog, Sheet, and Drawer always need a Title

`DialogTitle`, `SheetTitle`, `DrawerTitle` are required for accessibility. Use `className="sr-only"` if visually hidden.

```tsx
<DialogContent>
  <DialogHeader>
    <DialogTitle>Edit Profile</DialogTitle>
    <DialogDescription>Update your profile.</DialogDescription>
  </DialogHeader>
  ...
</DialogContent>
```

---

## Card structure

Use the sections needed by the card's actual content. A heading belongs in CardHeader/CardTitle, body content in CardContent, and footer actions in CardFooter. Omit sections that have no purpose instead of inventing descriptions or actions to complete the example:

```tsx
<Card>
  <CardHeader>
    <CardTitle>Team Members</CardTitle>
    <CardDescription>Manage your team.</CardDescription>
  </CardHeader>
  <CardContent>...</CardContent>
  <CardFooter>
    <Button>Invite</Button>
  </CardFooter>
</Card>
```

---

## Loading behavior follows the installed Button API

Check the local Button API before using loading props; a customized version may support them. When it does not, compose pending behavior with `Spinner`, supported icon placement, and `disabled`:

```tsx
<Button disabled>
  <Spinner data-icon="inline-start" />
  Saving...
</Button>
```

---

## TabsTrigger must be inside TabsList

Never render `TabsTrigger` directly inside `Tabs` — always wrap in `TabsList`:

```tsx
<Tabs defaultValue="account">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">...</TabsContent>
</Tabs>
```

---

## Provide an appropriate avatar fallback

Use AvatarFallback when an unavailable image would otherwise lose useful identity. Match existing fallback and accessible-label conventions; a decorative avatar may need a different treatment:

```tsx
<Avatar>
  <AvatarImage src="/avatar.png" alt="User" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>
```

---

## Use existing components instead of custom markup

Prefer these components when their semantics and styling fit the task. Existing accessible markup does not need replacement solely to follow this table.

| Instead of | Use |
|---|---|
| `<hr>` or `<div className="border-t">` | `<Separator />` |
| `<div className="animate-pulse">` with styled divs | `<Skeleton className="h-4 w-3/4" />` |
| `<span className="rounded-full bg-green-100 ...">` | `<Badge variant="secondary">` |
