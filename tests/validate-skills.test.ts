import { describe, expect, test } from "bun:test";

import { invocationPoliciesMatch } from "../scripts/invocation-policy.ts";

const implicitSkill = `---
name: example
description: Example skill.
---`;

const explicitSkill = `---
name: example
description: Example skill.
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
