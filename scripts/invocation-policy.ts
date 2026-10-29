import { asRecord, parseYamlRecord, readFrontmatter } from "./skill-frontmatter.ts";

type InvocationPolicies = {
  claudeExplicitOnly: boolean;
  codexExplicitOnly: boolean;
};

export function readInvocationPolicies(
  skillMarkdown: string,
  openAIYaml?: string,
): InvocationPolicies {
  const openAIPolicy = asRecord(parseYamlRecord(openAIYaml).policy);

  return {
    claudeExplicitOnly: readFrontmatter(skillMarkdown)["disable-model-invocation"] === true,
    codexExplicitOnly: openAIPolicy.allow_implicit_invocation === false,
  };
}

export function invocationPoliciesMatch(skillMarkdown: string, openAIYaml?: string): boolean {
  const policies = readInvocationPolicies(skillMarkdown, openAIYaml);
  return policies.claudeExplicitOnly === policies.codexExplicitOnly;
}
