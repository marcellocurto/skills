import { readdir } from "node:fs/promises";
import { join } from "node:path";

import { readInvocationPolicies } from "./invocation-policy.ts";

const repositoryRoot = join(import.meta.dir, "..");
const skillsRoot = join(repositoryRoot, "skills");
const manifestPath = join(repositoryRoot, ".claude-plugin", "plugin.json");

const entries = await readdir(skillsRoot, { withFileTypes: true });
const skillNames: string[] = [];

for (const entry of entries) {
  if (!entry.isDirectory()) continue;

  const skillFile = Bun.file(join(skillsRoot, entry.name, "SKILL.md"));
  if (await skillFile.exists()) skillNames.push(entry.name);
}

const manifest = (await Bun.file(manifestPath).json()) as { skills?: unknown };

if (
  !Array.isArray(manifest.skills) ||
  !manifest.skills.every((skill): skill is string => typeof skill === "string")
) {
  throw new Error(".claude-plugin/plugin.json must contain a string array named skills");
}

const expectedPaths = skillNames.toSorted().map((name) => `./skills/${name}`);
const declaredPaths = manifest.skills.toSorted();
const expectedSet = new Set(expectedPaths);
const declaredSet = new Set(declaredPaths);

const missingPaths = expectedPaths.filter((path) => !declaredSet.has(path));
const extraPaths = declaredPaths.filter((path) => !expectedSet.has(path));
const duplicatePaths = declaredPaths.filter((path, index) => declaredPaths.indexOf(path) !== index);
const invocationPolicyMismatches: string[] = [];

for (const skillName of skillNames) {
  const skillDirectory = join(skillsRoot, skillName);
  const skillMarkdown = await Bun.file(join(skillDirectory, "SKILL.md")).text();
  const openAIFile = Bun.file(join(skillDirectory, "agents", "openai.yaml"));
  const openAIYaml = (await openAIFile.exists()) ? await openAIFile.text() : undefined;
  const policies = readInvocationPolicies(skillMarkdown, openAIYaml);

  if (policies.claudeExplicitOnly !== policies.codexExplicitOnly) {
    invocationPolicyMismatches.push(
      `${skillName} (Claude: ${policies.claudeExplicitOnly ? "explicit only" : "implicit allowed"}; Codex: ${policies.codexExplicitOnly ? "explicit only" : "implicit allowed"})`,
    );
  }
}

if (
  missingPaths.length ||
  extraPaths.length ||
  duplicatePaths.length ||
  invocationPolicyMismatches.length
) {
  if (missingPaths.length) {
    console.error(`Missing manifest entries: ${missingPaths.join(", ")}`);
  }

  if (extraPaths.length) {
    console.error(`Unknown manifest entries: ${extraPaths.join(", ")}`);
  }

  if (duplicatePaths.length) {
    console.error(`Duplicate manifest entries: ${duplicatePaths.join(", ")}`);
  }

  if (invocationPolicyMismatches.length) {
    console.error(`Invocation policy mismatches: ${invocationPolicyMismatches.join(", ")}`);
  }

  process.exit(1);
}

console.log(`Validated ${skillNames.length} skills.`);
