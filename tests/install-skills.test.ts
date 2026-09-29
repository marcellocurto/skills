import { expect, test } from "bun:test";
import { publishedSkillNames, removedSkillNames } from "../scripts/install-skills.ts";

test("removes deleted or renamed managed skills without touching other sources", () => {
  const managed = { source: "marcellocurto/skills", sourceType: "github" };
  expect(
    removedSkillNames(
      {
        skills: {
          kept: managed,
          "old-name": managed,
          "address-review-feedback": managed,
          unrelated: { source: "someone/skills", sourceType: "github" },
          local: { source: "marcellocurto/skills", sourceType: "local" },
        },
      },
      ["kept", "new-name"],
    ),
  ).toEqual(["old-name", "address-review-feedback"]);
});

test("refuses ambiguous ownership and unsafe removal names", () => {
  expect(() => removedSkillNames({}, ["kept"])).toThrow();
  expect(() => removedSkillNames({ skills: {} }, [])).toThrow();
  expect(() =>
    removedSkillNames(
      { skills: { "--all": { source: "marcellocurto/skills", sourceType: "github" } } },
      ["kept"],
    ),
  ).toThrow();
});

test("requires a valid published inventory before allowing reconciliation", () => {
  expect(publishedSkillNames({ skills: ["./skills/kept", "./skills/new-name"] })).toEqual([
    "kept",
    "new-name",
  ]);
  for (const manifest of [{}, { skills: [] }, { skills: ["./skills/../other"] }]) {
    expect(() => publishedSkillNames(manifest)).toThrow();
  }
});
