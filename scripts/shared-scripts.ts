/**
 * A script that several skills need is copied into each skill's `scripts/`
 * directory under the same file name, because a skill runs scripts from its
 * own directory. Returns a label for each file name whose copies differ,
 * naming the skills that hold them, so the validator can keep the copies
 * identical.
 */
export function divergentSharedScripts(
  scripts: readonly { skill: string; name: string; content: string }[],
): string[] {
  const copiesByName = Map.groupBy(scripts, (script) => script.name);
  const divergent: string[] = [];

  for (const [name, copies] of copiesByName) {
    if (new Set(copies.map((copy) => copy.content)).size > 1) {
      divergent.push(`${name} (${copies.map((copy) => copy.skill).join(", ")})`);
    }
  }

  return divergent;
}
