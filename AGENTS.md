# Agent Instructions

Design and maintain all skills in this repository for use with GPT-6. Follow current GPT-6 prompting guidance when creating or revising a skill.

Skill descriptions should state the capability and semantic routing boundaries only. Put explicit-only behavior in supported invocation metadata—`disable-model-invocation: true` for Claude and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex—and never repeat that policy as prose in the description or body.

Skill runtime instructions must be self-contained and repository-controlled. Never use an external skill, prompt, principle file, or other mutable third-party document as runtime guidance from a `SKILL.md` or its supporting instruction files; write the required guidance locally instead. External source attribution belongs in `README.md`, and authoritative external documentation may be consulted only when the task itself requires current external facts—not as a substitute for maintained skill instructions.

In runtime instructions, reference other skills by name (for example, “Use the `tdd` skill when available”); the agent resolves their locations through the host's skill catalog. Do not use sibling paths such as `../tdd/SKILL.md`. Relative links are for supporting files within the same skill. Keep essential instructions local so missing companion skills do not remove required behavior.

Store every repository skill under `skills/<skill-name>/`. Keep `.claude-plugin/plugin.json` synchronized when adding, removing, or renaming a skill. Every repository skill must be listed in its `skills` array so installers group it under "Marcello Curto Skills" rather than "Other."

Also update `README.md` when adding or removing skills or the skill description materially changes.

Tests must protect intended behavior; never weaken them to hide a defect, and report unresolved failures honestly.

Repository tooling uses Bun, TypeScript 7, Oxlint, and Oxfmt. Run `bun run check` after changing tooling and `bun run format` before finishing.
