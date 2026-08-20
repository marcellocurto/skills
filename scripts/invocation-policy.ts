type InvocationPolicies = {
  claudeExplicitOnly: boolean;
  codexExplicitOnly: boolean;
};

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null ? (value as Record<string, unknown>) : {};
}

export function readInvocationPolicies(
  skillMarkdown: string,
  openAIYaml?: string,
): InvocationPolicies {
  const frontmatterSource = skillMarkdown.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  const frontmatter = frontmatterSource ? asRecord(Bun.YAML.parse(frontmatterSource)) : {};
  const openAIConfig = openAIYaml?.trim() ? asRecord(Bun.YAML.parse(openAIYaml)) : {};
  const openAIPolicy = asRecord(openAIConfig.policy);

  return {
    claudeExplicitOnly: frontmatter["disable-model-invocation"] === true,
    codexExplicitOnly: openAIPolicy.allow_implicit_invocation === false,
  };
}

export function invocationPoliciesMatch(skillMarkdown: string, openAIYaml?: string): boolean {
  const policies = readInvocationPolicies(skillMarkdown, openAIYaml);
  return policies.claudeExplicitOnly === policies.codexExplicitOnly;
}
