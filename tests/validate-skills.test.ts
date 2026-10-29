import { describe, expect, test } from "bun:test";

import { invocationPoliciesMatch } from "../scripts/invocation-policy.ts";
import { descriptionStatesWhenToUse } from "../scripts/skill-frontmatter.ts";

const implicitSkill = `---
name: example
description: Example skill. Use when testing.
---`;

const explicitSkill = `---
name: example
description: Example skill. Use when testing.
disable-model-invocation: true
---`;

const explicitOpenAI = `policy:
  allow_implicit_invocation: false`;

describe("invocation policy parity", () => {
  test("accepts implicit invocation for both agents", () => {
    expect(invocationPoliciesMatch(implicitSkill)).toBe(true);
  });

  test("accepts explicit-only invocation for both agents", () => {
    expect(invocationPoliciesMatch(explicitSkill, explicitOpenAI)).toBe(true);
  });

  test("rejects Claude-only explicit invocation", () => {
    expect(invocationPoliciesMatch(explicitSkill)).toBe(false);
  });

  test("rejects Codex-only explicit invocation", () => {
    expect(invocationPoliciesMatch(implicitSkill, explicitOpenAI)).toBe(false);
  });
});

describe("description routing", () => {
  test("accepts a description that says when to use the skill", () => {
    expect(descriptionStatesWhenToUse(implicitSkill)).toBe(true);
  });

  test("rejects a description that only says what the skill does", () => {
    expect(
      descriptionStatesWhenToUse(`---
name: example
description: Review pull requests.
---`),
    ).toBe(false);
  });

  test("rejects a skill without a description", () => {
    expect(descriptionStatesWhenToUse("---\nname: example\n---")).toBe(false);
  });
});
