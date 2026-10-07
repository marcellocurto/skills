---
name: ship-pr
description: Implement a GitHub issue or the work agreed in the conversation as a pull request, review it with independent agents for correctness, simplicity, security, and blast radius, then settle every review comment until Codex approves.
disable-model-invocation: true
---

# Ship PR

Take work from request to a settled pull request in four stages: build it and open the PR, review it with four independent agents, post their verified findings on the PR, and babysit the PR until every comment is answered. This skill runs the `implement-to-pr` and `babysit-pr` skills and adds the review between them. Never force-push or merge.

## 1. Build and open the PR

Follow the `implement-to-pr` skill through opening the pull request. Hold back its final response; its parts go into the report at the end. If it stops to ask the user something, this skill waits for the answer too.

Opening the PR starts Codex's review. The review below runs alongside it.

## 2. Review with four agents

Record the PR URL, the base branch, the head commit, and the merge base. Start four reviewers at the same time, one for each lens under **Lenses**. Choose each reviewer's agent type and model yourself from what the host offers, based on how much reasoning that lens needs for this diff; the four don't have to match. Don't push or change the checkout while they run.

Give each reviewer what an outside reviewer would have, and nothing from the implementation conversation, so its judgment stays independent:

- the PR URL, the base and head commits, the merge base, and the diff to review: `git diff <merge-base>..<head>`
- the requirements: the issue number, or the agreed request written out in full when there is no issue
- the repository's instruction files
- its lens, and the rules and return format below

Rules for every reviewer:

- Read only. Don't edit, commit, push, post comments, or resolve threads, and don't start other agents.
- Report only problems this PR causes or makes worse. Code outside the diff can be evidence, but a problem that already existed is not a finding.
- Don't run the full test suites; they already ran when the PR was built. Running one existing test, or a temporary probe placed outside the working tree and deleted afterward, is fine when it settles a finding.
- Back every finding with evidence from the code, tests, or requirements. Finding nothing material is a valid result.

Each reviewer returns what it inspected and what it skipped, plus each finding with:

- **Anchor:** a file and line range on the head side of the diff, chosen from the changed lines that cause the problem. When the harm lands outside the diff, such as a caller that breaks, anchor to the change that breaks it and name the affected location in the text.
- **Problem:** what triggers it and what goes wrong, or for a structural finding, which future change gets harder and why.
- **Evidence:** the code, test, or requirement that shows it.
- **Fix:** the focused change that resolves it.

If the host can't start agents, review each lens in a separate pass yourself, and say in the report that the passes were not independent.

## Lenses

### Correctness

Does the change do what the requirements ask, for every input and state its callers can produce? Check:

- behavior that is missing, partial, or contradicts the requirements
- invalid input, errors, empty and boundary cases, ordering, retries, races, and partial failure, where the change involves them
- whether the tests would fail if the changed behavior broke, naming the realistic regression that would slip through

Leave consumers outside the diff to Blast radius and trust boundaries to Security.

### Simplicity

Is the change as easy to understand and change as the problem allows? Simpler means easier to understand and change while keeping every requirement; fewer lines, functions, or files don't count by themselves. Check:

- behavior placed in a module that doesn't own its data and rules
- the same rule or fact kept in more than one place
- wrappers that only forward a call, and abstractions, configuration, or extension points no current requirement needs
- tangled control flow, interacting flags, hidden side effects, misleading names, and types that permit invalid states
- code that duplicates what the language, framework, a dependency, or an existing helper already provides
- leftover guards, fallbacks, and code that nothing uses

Each finding names a concrete simpler shape that keeps the required behavior and is worth its regression risk. Skip anything a formatter or linter enforces, and preferences without a concrete cost.

### Security

Review only the trust boundaries the change touches: user or external input, authentication and authorization, secrets and credentials, database queries, shell commands, file paths, rendered HTML, deserialization, new or upgraded dependencies, and data exposed in responses, logs, or errors. If the change touches none, say so and stop. Each finding needs a realistic path from an attacker or untrusted input to the harm. A guard against input that the types or callers already rule out is not a finding.

### Blast radius

What outside the edited files could break? List the contracts the change alters: signatures, return shapes, errors that callers match on, stored or serialized data, external APIs, CLI output, configuration and environment variables, timing and ordering, permission checks, and cost on hot paths. For each, find the consumers by symbol and by literal string, including generated code, configuration, scripts, migrations, other packages, and older versions still running during a rollout. A finding needs a plausible path from the change to a consumer that breaks. A search with no results is evidence, not proof, so say where you looked.

## 3. Post the verified findings

Wait for all four reviewers. Check each finding against the code yourself, since agreement between reviewers is not proof. Drop findings that are unsupported, already handled, pre-existing, outside the PR's intent, preference only, or speculative hardening; `babysit-pr` would reject them, and they only add noise to the PR. Merge findings that share one cause into one, under the lens that fits best.

Post the surviving findings as one pull request review with an inline comment for each. `babysit-pr` treats every unresolved review thread as open feedback, whoever wrote it, but it ignores conversation comments and review bodies from your own account, so a finding written only in the review body would never be settled. Use the `COMMENT` event, because GitHub doesn't let authors approve or request changes on their own PR, and pin the review to the reviewed head commit.

Start each inline comment with the lens and a short title in bold, then give the problem and the fix in two to four sentences. The review body is one line, such as "Reviewed `abc1234` for correctness, simplicity, security, and blast radius: 3 findings, inline." When no finding survives, post the review with only that line, ending in "nothing to change."

With `gh`, write the review to a JSON file outside the repository and post it:

```
gh api --hostname <host> repos/<owner>/<repo>/pulls/<number>/reviews --method POST --input <file>
```

```json
{
  "commit_id": "<head-sha>",
  "event": "COMMENT",
  "body": "Reviewed `abc1234` for correctness, simplicity, security, and blast radius: 2 findings, inline.",
  "comments": [
    { "path": "src/a.ts", "line": 42, "side": "RIGHT", "body": "**Correctness: ...** ..." },
    {
      "path": "src/b.ts",
      "start_line": 10,
      "start_side": "RIGHT",
      "line": 14,
      "side": "RIGHT",
      "body": "**Simplicity: ...** ..."
    }
  ]
}
```

GitHub rejects the whole review when one comment's lines are outside the diff. If that happens, move that anchor to a changed line in the same file that causes the problem, and post again. Read the review back to confirm it posted once with every comment. Before retrying an uncertain post, check the PR's reviews so you don't post twice.

## 4. Babysit

Run the `babysit-pr` skill on this PR. Its first check finds the review threads from step 3 along with anything Codex or people have posted, and settles them in one batch before it waits for more. It judges each finding as it would any reviewer's comment, so it can still reject one.

## Report

When `babysit-pr` finishes or stops, send one message that combines the final response from `implement-to-pr` with the report from `babysit-pr`. Use these parts in this order, and leave out any part with nothing to say:

```markdown
**PR:** the link, and one sentence on what it does.

**Status:** done, or why babysitting stopped, with the head commit and the number of rounds.

**Couldn't verify:** each check or tool that didn't run, what it would have caught, what you did instead, and what to install to run it.

**Judgment calls:** assumptions and decisions the issue or conversation didn't settle, and anywhere the work differs from what was asked.

**Feedback:** each review finding, labeled with its lens, and each Codex or human comment, with its outcome: fixed (with the commit), rejected (with the reason), or left open (with the decision needed). For an architectural problem, name the root cause and the change you recommend.

**Noticed, not done:** problems outside the scope that you found along the way.
```

Never say all checks pass when some didn't run. Name what passed and what didn't run.
