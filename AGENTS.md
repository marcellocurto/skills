# Agent Instructions

Design and maintain all skills in this repository for use with the GPT-5.6 model family. Follow current GPT-5.6 prompting guidance when creating or revising a skill.

Skill descriptions should state the capability and semantic routing boundaries only. Put explicit-only behavior in supported invocation metadata—`disable-model-invocation: true` for Claude and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex—and never repeat that policy as prose in the description or body.

Skill runtime instructions must be self-contained and repository-controlled. Never use an external skill, prompt, principle file, or other mutable third-party document as runtime guidance from a `SKILL.md` or its supporting instruction files; write the required guidance locally instead. External source attribution belongs in `README.md`, and authoritative external documentation may be consulted only when the task itself requires current external facts—not as a substitute for maintained skill instructions.

Treat external skills as research, not templates. Extract the useful decisions, then write from scratch in this repository's vocabulary and voice. Do not copy their prose, headings, examples, slogans, structure, tone, or workflow ceremony. Remove generic advice, repetition, hype, and any sentence that does not change agent behavior.

Store every repository skill under `skills/<skill-name>/`. Keep `.claude-plugin/plugin.json` synchronized when adding, removing, or renaming a skill. Every repository skill must be listed in its `skills` array so installers group it under "Marcello Curto Skills" rather than "Other."

Also update `README.md` when adding or removing skills or the skill description materially changes.

Repository tooling uses Bun, TypeScript 7, Oxlint, and Oxfmt. Run `bun run check` after changing tooling and `bun run format` before finishing.
