# Good and Bad Tests

## Good Tests

**Contract-focused**: Exercise the behavior through the interface that owns it, whether public or internal. Use real collaborators when their behavior is part of the claim.

```typescript
// GOOD: Tests observable behavior
test("checkout returns confirmation for a valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

This checks the returned outcome. Persistence or payment effects need their own observations when they are part of the contract.

Characteristics:

- Tests behavior users/callers care about
- Uses a meaningful public or internal interface
- Survives implementation-only refactors of the tested contract
- Describes WHAT, not HOW
- Assertions together establish one coherent behavior

## Match the evidence to the contract

**Implementation-detail tests** assert a private arrangement the contract does not promise. Checking that a particular helper ran can pass even when the required result is wrong. An interaction assertion is useful when that interaction is itself the promised effect, such as dispatching exactly one payment request for duplicate submissions.

Judge these mechanisms by what they prove:

| Contract | Useful evidence | Insufficient substitute |
| --- | --- | --- |
| A created user can be retrieved | Create and retrieve through the supported interface | A database row alone, without exercising retrieval |
| A write persists the required record | Inspect the real test database using the new record's identity | A mock database method was called |
| Failed work rolls back atomically | Observe the relevant database state after rollback | A rollback helper was invoked |
| Duplicate submissions dispatch one payment request | Observe requests at the payment boundary | A private deduplication helper ran a particular number of times |
| An internal policy enforces a domain invariant | Exercise that policy's interface with a case that violates the invariant | Assert its private fields or intermediate helper sequence |
| Existing recipients can save invoices after an upgrade | Call the invoice save operation with representative existing assignments and observe the saved number | Initialize a new allocator in setup when the upgrade does not guarantee initialization |
| A deployed capability is available | Exercise its selected configuration and required outcome | Verify only that missing configuration produces a graceful error |

Direct database observations are appropriate when persistence, schema, or transaction behavior is the subject. If the promise is committed state visible to another consumer, observe it after commit through an independent connection or the actual consumer path. A public read method may be the better observation for a user-facing retrieval contract:

```typescript
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

Do not create a public API merely to avoid testing an existing internal contract. Equally, do not reach into private state when the same contract can be tested through its owning interface.

## When a regression should stay red

Suppose two existing recipients legitimately share customer number `25081`. A regression calls the real invoice creation operation for each and checks that both saved invoices retain `25081`. If the implementation rejects the second recipient, expecting that rejection would encode the defect. Giving the recipients different numbers, running an unguaranteed import first, or stubbing number assignment would remove the case the test must protect.

Keep the expectation while fixing the assignment model within scope. If that requires an unresolved domain decision or unapproved migration, retain the failure and report the blocker. If the user instead explicitly changes the contract to require distinct numbers, update the test against that decision and explain which former behavior is being retired.

## Independent expectations

Repeating the production calculation in a test can reproduce its mistakes. That is a reason to seek an independent oracle, not proof that every calculated expectation is tautological.

```typescript
// Weak oracle if it duplicates the production calculation and its assumptions.
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// A worked example supplies an independent expected result.
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
