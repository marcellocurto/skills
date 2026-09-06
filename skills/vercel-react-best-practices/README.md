# React Performance Guidance

This directory contains repository-maintained guidance adapted from Vercel Agent Skills. Runtime work starts with `SKILL.md` and loads only the rules relevant to the task. `AGENTS.md` is the compiled reference for deliberate full-guide reading.

## Sources of truth

- `SKILL.md`: applicability, evidence standards, and the rule index.
- `rules/*.md`: canonical rule guidance and examples.
- `rules/_sections.md`: category order and descriptions.
- `rules/_template.md`: starting format for a new rule.
- `metadata.json`: compiled-document metadata.
- `AGENTS.md`: generated from the rules and metadata; do not edit its rule copies independently.

## Maintain the guide

Edit the canonical rule first, including its conditions, protected contracts, and examples. Update the `SKILL.md` index when a rule is added, removed, or its summary changes. Impact ratings prioritize investigation; numerical examples need their workload and provenance and are not measured results for the user's application.

From the repository root, regenerate the compiled reference:

```bash
bun run react-guidance:build
```

Check that the compiled content is current:

```bash
bun run react-guidance:check
```

The compiler preserves rule code blocks and adjusts prose headings and relative rule links for the compiled document. It includes every non-underscore Markdown rule in its category. Keep required applicability guidance in the canonical rule so it also appears in the compiled reference.

Run `bun run format` and `bun run check` from the repository root. The full check includes compiled-reference synchronization. This checkout does not use the upstream `pnpm build`, `pnpm validate`, or test-case extraction commands.

## Primary references

- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
- [React cache](https://react.dev/reference/react/cache)
- [SWR](https://github.com/vercel/swr)
- [better-all](https://github.com/shuding/better-all)
- [lru-cache](https://isaacs.github.io/node-lru-cache/)
