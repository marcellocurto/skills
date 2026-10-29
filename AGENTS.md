# Agent Instructions

State only capability and routing boundaries in skill descriptions: what the skill does, then a "Use when" clause naming the requests or situations that should load it. Name a task situation instead of a user request for skills that should load without being asked, and add "when another skill runs it" for skills that other skills call. `bun run validate:skills` rejects descriptions without the clause. Prefer model invocation; make a skill explicit-only only when a loose match could cause effects that are hard to undo, such as production migrations. Mark explicit-only skills in invocation metadata — `disable-model-invocation: true` for Claude, `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex — never as prose in description or body.

Keep `SKILL.md` and supporting runtime instructions self-contained and repository-controlled. Never delegate runtime guidance to an external skill, prompt, principle file, or other mutable third-party document; write it locally. Attribute external sources in `README.md`. Consult authoritative external docs only when the task needs current external facts, never as a substitute for maintained instructions.

Reference other skills by name in runtime instructions (for example, “Use the `tdd` skill when available”); the host catalog resolves locations. Never use sibling paths like `../tdd/SKILL.md`. Reserve relative links for supporting files in the same skill, and keep essential instructions local so a missing companion skill removes nothing required. The exception is an orchestrator skill that exists to run other skills in sequence, such as `ship-pr`: it names the skills it runs and writes locally only the steps it adds.

Store every skill under `skills/<skill-name>/` and keep it listed in `.claude-plugin/plugin.json`'s `skills` array (groups it under "Marcello Curto Skills") when adding, removing, or renaming.

Update `README.md` when skills are added/removed or a description materially changes.

Tests must protect intended behavior; never weaken them to hide a defect, and report unresolved failures honestly.

Tooling: Bun, TypeScript 7, Oxlint, Oxfmt. Run `bun run check` after tooling changes, `bun run format` before finishing.
