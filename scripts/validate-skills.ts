import { readdir } from "node:fs/promises";
import { join } from "node:path";

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

if (missingPaths.length || extraPaths.length || duplicatePaths.length) {
  if (missingPaths.length) {
    console.error(`Missing manifest entries: ${missingPaths.join(", ")}`);
  }

  if (extraPaths.length) {
    console.error(`Unknown manifest entries: ${extraPaths.join(", ")}`);
  }

  if (duplicatePaths.length) {
    console.error(`Duplicate manifest entries: ${duplicatePaths.join(", ")}`);
  }

  process.exit(1);
}

console.log(`Validated ${skillNames.length} skills.`);
