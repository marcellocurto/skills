# Reviewers

This file defines the independent reviewers `babysit-pr` starts: the first review of a pull request, and the fix check before each push. Choose each reviewer's agent type and model yourself from what the host offers, based on how much reasoning its lens needs for this diff; reviewers don't have to match. If the host can't start agents, review each lens in a separate pass yourself, and say in the report that the passes were not independent.

## What every reviewer gets

Give each reviewer what an outside reviewer would have, and nothing from the implementation conversation, so its judgment stays independent:

- the PR URL, the base and head commits, the merge base, and the diff it reviews
- the requirements: the issue number, or the agreed request written out in full when there is no issue
- the PR description's risks and non-goals, and the issue's non-goals
- the repository's instruction files, including any review decisions and realistic input sizes they record
- its lens, and the rules and return format below

## Rules for every reviewer

- Read only. Don't edit, commit, push, post comments, or resolve threads, and don't start other agents.
- Report only problems this PR causes or makes worse. Code outside the diff can be evidence, but a problem that already existed is not a finding.
- Anything the PR's risks and non-goals, the issue's non-goals, or the repository's instruction files already decide is not a finding.
- Judge cost and edge cases against realistic input: the sizes the repository's instructions state, otherwise what its validators, fixtures, and seed data show. Name the size you assumed. A crafted file, or an input that validation or the types already reject, is a trigger only under the Security lens or when you reproduced the harm.
- Don't run the full test suites; they ran before the PR was pushed. For each candidate finding, try to reproduce it with one existing test or a temporary probe placed outside the working tree and deleted afterward, when that takes a few minutes. Skip the attempt for races, deploy ordering, and other cases a quick probe can't show.
- Back every finding with evidence from the code, tests, or requirements. Finding nothing material is a valid result.

## Return format

Each reviewer returns what it inspected and what it skipped, plus each finding with:

- **Anchor:** a file and line range on the head side of the diff, chosen from the changed lines that cause the problem. When the harm lands outside the diff, such as a caller that breaks, anchor to the change that breaks it and name the affected location in the text.
- **Problem:** what goes wrong, or for a structural finding, which future change gets harder and why.
- **Trigger:** the user action, data, or deploy step that produces it on the current deployment.
- **Outcome:** a security hole, data loss, a crash, a stuck job, or a wrong result; or none of these, for a structural or minor problem.
- **Evidence:** _reproduced_, with the probe or test and what it showed, or _reasoned_, with the code path.
- **Fix:** the focused change that resolves it.

## Lenses

Correctness, Simplicity, Security, and Blast radius review every pull request. Scenarios, Rollout, and Specification review it when the diff matches their condition; decide that from the files and code the diff touches.

### Correctness

Does the change do what the requirements ask, for every input and state its callers can produce? Check:

- behavior that is missing, partial, or contradicts the requirements
- each guarantee the PR description, doc comments, or contract types make, traced through every exit path of the changed functions: early returns, `?`, `break`, and caught errors that skip a promised check or discard a result already computed
- what a deleted or replaced path enforced, such as a validation, trigger, or ordering rule, and where the new path enforces it, or that the PR drops it on purpose
- arithmetic on realistic values: sums, rounding, and comparisons against limits, evaluated with concrete numbers and compared with the tolerance the validator uses elsewhere; and integer sizes at the realistic maximum
- invalid input, errors, empty and boundary cases, ordering, retries, races, and partial failure, where the change involves them
- whether the tests would fail if the changed behavior broke, naming the realistic regression that would slip through

Leave workflows outside the diff to Scenarios, consumers to Blast radius, and trust boundaries to Security.

### Scenarios

Runs when the change writes, reads, or derives state that outlives one request: database rows, files, external records, queued or scheduled jobs, caches, or drafts saved in the browser.

List each stored field, derived value, or invariant the change adds or relies on. Find every workflow outside the diff that writes or reads it, by symbol and by column or field name, such as reopening a draft, correction, cancellation, deletion, revision, restoring an interrupted save, background jobs, retry and resume after a partial failure, and edits or deletions in an external system. For each, play one concrete scenario through to the stored or shown result.

For each new job, action, or chain of writes, list every commit and remote-call boundary and say what happens if the process stops right after it: what reschedules or settles the work, and whether a retry can succeed. For each remote call, check cancellation, idempotency, and recorded usage on every terminal path, and compare with the repository's existing helper for that provider.

Where the repository already handles the same entity or mode on another path, compare the two paths' rules. Report only scenarios that end in a wrong result, lost data, or a stuck state.

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

What outside the edited files could break? List the contracts the change alters: signatures, return shapes, errors that callers match on, external APIs, CLI output, configuration and environment variables, timing and ordering, permission checks, build steps, and cost on hot paths. For each, find the consumers by symbol and by literal string, including generated code, configuration, scripts, other packages, and code that runs in a different environment, such as a server component importing client code. A finding needs a plausible path from the change to a consumer that breaks. A search with no results is evidence, not proof, so say where you looked. Leave stored data and releases to Rollout.

### Rollout

Runs when the diff touches server functions or API contracts, stored data shapes, schemas, migrations, background job payloads, or deploy and infrastructure files.

Read the repository's release procedure and its policy for the previous release from its instructions and deploy docs, then check against them:

- each changed function signature, return shape, validator, and stored enum value, against the clients, workers, and open browser tabs from the previous release that the policy says must keep working
- each migration or backfill while the old release keeps writing until the switch: can those writes make it or its constraints fail
- rows that earlier releases created, such as records from before a table or field existed, against each invariant the new code assumes
- serialized state that outlives a deploy, such as saved plans, job payloads, and journals, when the next release reads it
- each manual cutover or deploy step the PR documents, walked in order: what it changes or destroys, and what would restore it
- the rollback path, where the policy requires one

A finding names the release state and the step at which it breaks.

### Specification

Runs when the change parses or emits a third-party file format or protocol, or relies on a provider API's documented behavior, such as OOXML, MSG, HTTP streaming, database locking, CI workflow syntax, or a payment or model provider's API.

Read the vendor's documentation for the constructs the change handles, fetching it when the host has web access, and cite the section on every finding. Check only constructs that the applications producing this input actually write, and compare with what the third-party library the code relies on does with the same construct. A construct the specification allows but no real producer writes is not a finding.

## First review

Record the PR URL, the base branch, the head commit, and the merge base. Choose the lenses, then start one reviewer per lens at the same time, each with the diff `git diff <merge-base>..<head>`. Don't push or change the checkout while they run.

Wait for all reviewers. Check each finding against the code yourself, since agreement between reviewers is not proof. Drop findings that are unsupported, already handled, pre-existing, outside the PR's intent, decided by the non-goals or the repository's instructions, preference only, or speculative hardening; reasoned findings whose trigger is a crafted input or input that validation rejects, unless the lens is Security; and findings that fall short of the fix bar in `SKILL.md`. Merge findings that share one cause into one, under the lens that fits best.

Post the surviving findings as one pull request review with an inline comment for each, so each becomes a review thread that a round settles. Use the `COMMENT` event, because GitHub doesn't let authors approve or request changes on their own PR, and pin the review to the reviewed head commit.

Start each inline comment with the lens and a short title in bold, followed by _(reproduced)_ when the evidence was reproduced. Then give the problem, its trigger, and the fix in two to four sentences. The review body is one line naming the lenses that ran, such as "Reviewed `abc1234` for correctness, scenarios, simplicity, security, and blast radius: 3 findings, inline." When no finding survives, post the review with only that line, ending in "nothing to change." `watch_pr.py` recognizes the first review by the body's opening "Reviewed \`", so keep that wording.

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
    { "path": "src/a.ts", "line": 42, "side": "RIGHT", "body": "**Correctness: ...** _(reproduced)_ ..." },
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

## Fix check

Start one reviewer after a round's fixes are committed and before they are pushed. Give it, besides what every reviewer gets:

- the round's diff: `git diff <last-reviewed-commit>..HEAD`; for a round's second fix check, it starts at the commit the first check reviewed
- every change since the first review: `git diff <first-reviewed-commit>..HEAD`
- the threads this round answers, each with the reply you drafted
- every finding from earlier rounds that you rejected or accepted as a limit, with the reason
- whether this is a late round

Both commits come from the `reviews` field of `watch_pr.py`. When the commits since one of them include a merge from the base branch, give the reviewer `git log -p --no-merges <commit>..HEAD ^origin/<base>` instead of that diff, so the base branch's own changes stay out.

Ask it three questions, and apply the Correctness and Scenarios lenses, plus Rollout or Specification when their condition matches, to the code the round adds:

1. Does each fix do what its drafted reply claims, on every path?
2. What does the round break? Look for a check moved after work it should guard, a fallible call before the step that schedules recovery, an early return that drops a result already computed, and a guarantee the code made before the round that it no longer makes.
3. Which additions since the first review could shrink, merge into one fix at a shared cause, or be reverted, while still handling every finding that met the fix bar?

It reports only problems that meet the fix bar in `SKILL.md`, and simplifications that remove more code than they add. It doesn't raise points the rejected and accepted findings already settle. In a late round, it reports only security holes, data loss, crashes, stuck jobs, wrong results on realistic input, and changes that remove more code than they add.

Its findings don't become threads. Check each against the code yourself, as for the first review, and fix the survivors in the same push. After the push, post a review with no inline comments, pinned to the pushed head, whose body is one line such as "Reviewed the fixes in `abc1234`: 2 findings fixed before this push." or "Reviewed the fixes in `abc1234`: nothing to change." `watch_pr.py` counts fix checks and recognizes a reviewed head by that opening, so keep the wording.
