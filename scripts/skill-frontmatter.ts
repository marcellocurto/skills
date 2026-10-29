export function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null ? (value as Record<string, unknown>) : {};
}

export function parseYamlRecord(source: string | undefined): Record<string, unknown> {
  return source?.trim() ? asRecord(Bun.YAML.parse(source)) : {};
}

export function readFrontmatter(skillMarkdown: string): Record<string, unknown> {
  return parseYamlRecord(skillMarkdown.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1]);
}

/**
 * Hosts pick skills by matching the request against the description, so each
 * description must say when to use the skill as well as what it does.
 */
export function descriptionStatesWhenToUse(skillMarkdown: string): boolean {
  const { description } = readFrontmatter(skillMarkdown);
  return typeof description === "string" && /\bUse when\b/.test(description);
}
