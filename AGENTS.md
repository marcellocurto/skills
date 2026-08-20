# Agent Instructions

Design and maintain all skills in this repository for use with the GPT-5.6 model family. Follow current GPT-5.6 prompting guidance when creating or revising a skill.

Skill descriptions should state the capability and semantic routing boundaries only. Put explicit-only behavior in supported invocation metadata—`disable-model-invocation: true` for Claude and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex—and never repeat that policy as prose in the description or body.

Store every repository skill under `skills/<skill-name>/`. Keep `.claude-plugin/plugin.json` synchronized when adding, removing, or renaming a skill. Every repository skill must be listed in its `skills` array so installers group it under "Marcello Curto Skills" rather than "Other."

Also update `README.md` when adding or removing skills or the skill description materially changes.

Repository tooling uses Bun, TypeScript 7, Oxlint, and Oxfmt. Run `bun run check` after changing tooling and `bun run format` before finishing.
