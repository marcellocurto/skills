import { describe, expect, test } from "bun:test";

import { invocationPoliciesMatch } from "../scripts/invocation-policy.ts";
import { descriptionStatesWhenToUse } from "../scripts/skill-frontmatter.ts";
import { divergentSharedScripts } from "../scripts/shared-scripts.ts";
import { referencedSkillNames } from "../scripts/skill-references.ts";

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

describe("skill references", () => {
  test("finds skills named singly and in lists", () => {
    expect(
      referencedSkillNames(
        "Use the `tdd` skill when available. This skill runs the `implement-to-pr` and `babysit-pr` skills, then the `a`, `b`, or `c` skills.",
      ).toSorted(),
    ).toEqual(["a", "b", "babysit-pr", "c", "implement-to-pr", "tdd"]);
  });

  test("ignores code that is not named as a skill", () => {
    expect(referencedSkillNames("Run `bun test` and read `skill-path`.")).toEqual([]);
  });
});

describe("shared scripts", () => {
  test("accepts identical copies and scripts with distinct names", () => {
    expect(
      divergentSharedScripts([
        { skill: "a", name: "fetch.py", content: "same" },
        { skill: "b", name: "fetch.py", content: "same" },
        { skill: "b", name: "other.py", content: "different" },
      ]),
    ).toEqual([]);
  });

  test("reports copies that differ", () => {
    expect(
      divergentSharedScripts([
        { skill: "a", name: "fetch.py", content: "one" },
        { skill: "b", name: "fetch.py", content: "two" },
      ]),
    ).toEqual(["fetch.py (a, b)"]);
  });
});
