/**
 * Skills name the skills they run as "the `name` skill" or "the `a` and `b`
 * skills". Returns every name written that way, so the validator can check
 * that each one exists in this repository.
 */
export function referencedSkillNames(markdown: string): string[] {
  const names = new Set<string>();
  const mention = /((?:`[a-z][a-z0-9-]*`(?:,? (?:and|or) |, )?)+) skills?\b/g;

  for (const [, list = ""] of markdown.matchAll(mention)) {
    for (const [, name] of list.matchAll(/`([a-z][a-z0-9-]*)`/g)) {
      if (name) names.add(name);
    }
  }

  return [...names];
}
