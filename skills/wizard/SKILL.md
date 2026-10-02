---
name: wizard
description: Create an interactive Bash wizard for setup steps that only a human can complete.
---

# Wizard

A **wizard** is a Bash script that guides a human through a manual procedure. It opens each URL, explains what to click and copy, captures values, writes them to the intended destinations, and shows progress. It might configure third-party services, run a one-off migration, or move the project from one state to another.

[template.sh](template.sh) provides stage-by-stage progress, confirmation gates, cross-platform URL opening (including WSL), hidden secret entry, idempotent `.env` upserts, `gh secret`/`gh variable` writes, and a closing summary. Scope the procedure and author its stages without hand-editing the shared library above the `STAGES` marker.

A wizard is ephemeral by default: save it to a scratch path for the requested run. When the user wants a repeatable setup path in the repository, retain it under the project's script conventions and document how to run it. Repeatability does not authorize a commit; commit only when the user has authorized that action.

## Process

### 1. Scope the procedure

Identify the steps and values needed for the requested setup, migration, or transition. Read relevant repository context before asking for information:

- For setup: relevant environment examples, README instructions, service and framework configuration, and CI workflows. Use `secrets.*` / `vars.*` references to identify consumers of the requested setup's values; unrelated references do not expand the wizard's scope. Reuse existing configuration where appropriate instead of collecting credentials again. Inspect secret-bearing files only as needed, without exposing their values.
- For a migration or transition: the current state, the target state, and the irreversible actions between them.

Reuse the procedure and decisions already established in the conversation. A stage outline can be a progress update; it does not require another approval round. Ask only about unresolved choices that materially affect the procedure, target, or captured values, and continue preparing independent stages while those choices remain open. The human runs the finished script, so its `confirm` gates are where consequential actions get approved; do not run it yourself.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written (`.env`, a GitHub secret, both, or nowhere; some stages are pure actions), and (c) whether it's secret (hidden entry) or public.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where a value is shown, which variable it fills: e.g. "Dashboard → Developers → API keys → Reveal test key → copy". Where you don't actually know the current UI or the exact command, say so and ask the user or check the docs: never invent steps that may not exist.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` per step, in dependency order. Use the library helpers: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`. Set `TOTAL_STAGES` to the number of stages you wrote.

Open the URL before asking for its value. Use `ask_secret` for secrets; never embed captured secrets in the script or print them. Persist each value only to its scoped destination: `write_env` for local environment files and `set_secret`/`set_var` for the relevant GitHub configuration. Do not copy a value to additional destinations merely because helpers exist.

Before each irreversible operation, show its target and consequence and require `confirm` to succeed before executing it. A declined confirmation must skip or abort the action; the banner's readiness pause is not a substitute. Keep these execution gates even when the user has authorized preparing the script.

Each `stage` and `finish` waits for Enter and then clears the screen, so the human reads a stage's confirmations and warnings before the next one starts. Keep a stage to one focused task so everything it shows fits on screen. Don't touch the library above the marker.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available.
- `chmod +x <script>`.
- Don't run it end-to-end yourself: it opens browsers and blocks on human input. Trace it statically instead: required values are captured or reused, each write reaches its intended destination, CI secret and variable names match the relevant consumers, and irreversible operations cannot run after a declined confirmation.
- Deliver the script with run instructions, say which repository its `gh` writes target (it uses the repository of the directory it runs in), and identify consequential stages that require human confirmation. Completion means the requested script is ready for the human to run; do not claim the setup or migration has executed.
