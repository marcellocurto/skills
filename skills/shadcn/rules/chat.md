# Chat & Messaging

Prefer these conversation primitives when available and suited to the task.
Preserve established chat components when they already meet the requirements.
The composition APIs below apply when choosing these primitives; presentation
examples do not forbid other accessible designs.

Install: `npx shadcn@latest add message-scroller message bubble attachment marker`

The same component names and props ship for both `base` and `radix`; only
composition differs (`render` vs `asChild`). See [base-vs-radix.md](./base-vs-radix.md).

## Contents

- Scrollable threads use MessageScroller
- Message rows use Message
- Message surfaces use Bubble
- Attachments use Attachment
- System notes and dividers use Marker
- Streaming, anchoring, and jump-to-latest are built in
- Escape hatch: the scroller hooks

---

## Scrollable threads use MessageScroller

Prefer `MessageScroller` when its APIs cover the required scrolling, following,
position restoration, or jump behavior. Avoid duplicating those features, but
do not replace an existing implementation solely to follow this default.

The parts nest in a fixed order. Every direct child of the content is wrapped in
a `MessageScrollerItem` so the scroller can measure, anchor, preserve position,
track visibility, and jump to it. `MessageScrollerButton` sits inside
`MessageScroller`, after the viewport.

**Custom implementation:**

```tsx
// Hand-rolled scroll container with manual stick-to-bottom logic.
<div ref={scrollRef} onScroll={handleScroll} className="flex-1 overflow-y-auto">
  <div className="flex flex-col gap-6 p-4">
    {messages.map((m) => (
      <ChatMessage key={m.id} message={m} />
    ))}
  </div>
</div>
```

**Component composition:**

```tsx
<MessageScrollerProvider autoScroll>
  <MessageScroller>
    <MessageScrollerViewport>
      <MessageScrollerContent>
        {messages.map((message) => (
          <MessageScrollerItem
            key={message.id}
            messageId={message.id}
            scrollAnchor={message.role === "user"}
          >
            <Message align={message.role === "user" ? "end" : "start"}>
              {/* ...message content... */}
            </Message>
          </MessageScrollerItem>
        ))}
      </MessageScrollerContent>
    </MessageScrollerViewport>
    <MessageScrollerButton />
  </MessageScroller>
</MessageScrollerProvider>
```

---

## Message rows use Message

`Message` lays out a single row: avatar, header, content, footer, with
alignment. Group consecutive rows from one sender with `MessageGroup`. Don't
rebuild the row from flex divs.

`align="end"` is the current user's side; `align="start"` is everyone else.

```tsx
<Message align="start">
  <MessageAvatar>
    <Avatar>
      <AvatarImage src={sender.avatar} alt={sender.name} />
      <AvatarFallback>{initials}</AvatarFallback>
    </Avatar>
  </MessageAvatar>
  <MessageContent>
    <MessageHeader>{sender.name}</MessageHeader>
    <Bubble>
      <BubbleContent>{text}</BubbleContent>
    </Bubble>
    <MessageFooter>{time}</MessageFooter>
  </MessageContent>
</Message>
```

---

## Message surfaces use Bubble

Prefer `Bubble` + `BubbleContent` for a message surface when their variants fit
the requested design. Existing custom surfaces may remain appropriate.

- `variant`: `default`, `secondary`, `muted`, `tinted`, `outline`, `ghost`, `destructive`.
- `align`: `start` or `end` (matches the `Message` side).

`BubbleReactions` renders the reaction cluster. `side` (`top` | `bottom`) and
`align` (`start` | `end`) position it against the bubble. Prefer those APIs
before adding custom positioning.

**Custom implementation:**

```tsx
<div className="w-fit rounded-2xl bg-primary px-3 py-2 text-primary-foreground">
  {text}
</div>
```

**Component composition:**

```tsx
<Bubble variant="default" align="end">
  <BubbleContent>{text}</BubbleContent>
  <BubbleReactions side="bottom" align="end">
    <Badge variant="secondary">👍 2</Badge>
  </BubbleReactions>
</Bubble>
```

---

## Attachments use Attachment

Prefer `Attachment` for file and image attachments when its presentation and
states fit. When using it, wire `state` to the real upload status rather than
duplicating the component's feedback with a separate spinner.

- `state`: `idle`, `uploading`, `processing`, `error`, `done`. `uploading` and
  `processing` apply the `shimmer` animation to the title automatically.
- `size`: `default`, `sm`, `xs`. `orientation`: `horizontal`, `vertical`.
- Use `AttachmentGroup` to lay out several attachments in a scrolling row.

```tsx
<Attachment state="done">
  <AttachmentMedia variant="icon">
    <FileTextIcon />
  </AttachmentMedia>
  <AttachmentContent>
    <AttachmentTitle>homepage-feedback.pdf</AttachmentTitle>
    <AttachmentDescription>PDF · 2.4 MB</AttachmentDescription>
  </AttachmentContent>
  <AttachmentActions>
    <AttachmentAction>
      <DownloadIcon />
    </AttachmentAction>
  </AttachmentActions>
</Attachment>
```

For an image, use `<AttachmentMedia variant="image">` with an `img` child.

---

## System notes and dividers use Marker

Prefer `Marker` for status lines ("Sarah joined the conversation"), date
dividers ("Today"), and labeled separators when it matches the product pattern.

- `variant`: `default` (plain row), `separator` (centered label with rules on
  each side), `border` (bottom-bordered row).
- `MarkerIcon` holds a leading icon; `MarkerContent` holds the label.

**Custom implementation:**

```tsx
<div className="flex items-center gap-3 py-2">
  <Separator className="flex-1" />
  <span className="text-xs text-muted-foreground">Today</span>
  <Separator className="flex-1" />
</div>
```

**Component composition:**

```tsx
<Marker variant="separator">
  <MarkerContent>Today</MarkerContent>
</Marker>
```

---

## Streaming, anchoring, and jump-to-latest are built in

When using `MessageScroller`, use its built-in behavior before introducing
another follow-scroll hook, observer, or scroll-position calculation.

- **Follow the live edge while streaming.** `MessageScrollerProvider` with
  `autoScroll` keeps the view pinned to new content and yields the moment the
  user scrolls up. Streaming token updates that grow the last message are
  followed automatically.
- **Anchor a turn.** `scrollAnchor` on a `MessageScrollerItem` marks the row to
  hold in view (typically the user's message that started the turn).
- **Jump to latest.** `MessageScrollerButton` appears when the user scrolls away
  and scrolls back on click. `direction="end"` (default) or `direction="start"`.
  It is a self-managing control, so don't gate it behind your own scroll-position
  state.

For a "thinking…" indicator while the model generates, prefer the available
`shimmer` utility when it matches the requested treatment. See
[styling.md](./styling.md).

---

## Escape hatch: the scroller hooks

For behavior the parts don't expose, read state from the hooks rather than
re-implementing the scroller: `useMessageScroller`,
`useMessageScrollerVisibility`, and `useMessageScrollerScrollable`. They come
from the auto-installed `@shadcn/react` dependency, so there's nothing extra to
install. Reach for them only when composition can't express what you need.
