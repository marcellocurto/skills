---
name: code-review
description: Review a specific diff, pull request, or commit range with independent reviewers for correctness, security, maintainability, and repository rules, check each finding against the code, and check fixes against earlier findings. Use when the user asks to review changes, a PR, or commits, or when another skill runs it to review a change or check fixes. Not for whole-codebase or current-state subsystem audits.
---

# Code Review

Review one exact change and report the problems it introduces or worsens, each checked against the code. This is read-only: don't edit files, add tests, apply fixes, commit, push, post comments, or resolve threads. Name a credential committed to the code only by its file and line, never copying its value into a brief, finding, or report.

The reviewers' instructions, lenses, and return format, and the **Verifier**, are in [REVIEWERS.md](REVIEWERS.md).

This skill decides whether a problem is real, how much harm it causes, and whether the change caused it. Whether and when to fix it belongs to the person or skill that asked. Report every problem the change introduces or worsens with the Outcome the evidence supports, and don't hold one back because it seems minor or not worth another round.

It runs in one of three modes:

- **Standalone,** when a person asks for the review: report to them with verdicts, as under **Report**.
- **Review for another skill,** such as `babysit-pr` reviewing a new PR: return findings as under **Return to the caller**.
- **Fix check for another skill:** check commits that fix earlier findings, as under **Fix check**, and return findings the same way.

If the host can't start agents, do each reviewer's work, including the Verifier's, in a separate local pass, even for a change you wrote, and report that the passes weren't independent.

Check that the agents this skill starts leave the checkout as they found it. Before each group starts, whether reviewers, a fix-check reviewer, or verifiers, record the branch, the commit, and the output of `git status --porcelain`. When the group has returned, compare. Undo what differs: return to the recorded branch and commit, restore a tracked file that had no uncommitted changes before, and delete a file that wasn't there. That is the one change this skill makes to a checkout. A changed path that already had uncommitted changes can't be recovered, so stop and tell the user or calling skill which paths those are.

## 1. Pin the change

Review the pull request, branch, commit range, or working changes the user or calling skill names. If none is named, review the current branch against the default branch plus uncommitted changes. Record the base and head commits and the merge base, and review `git diff <merge-base>..<head>` with its commit list. For working changes, include staged, unstaged, and relevant untracked files.

## 2. Gather the requirements

Requirements come from these sources, highest priority first:

1. the user's latest decisions in the conversation, or the decisions a calling skill passes on
2. a named specification, or the same-repository issue the change closes
3. the pull-request description
4. commit messages, and intent inferred from the code

A pull-request description or commit message states intent, risks, and non-goals. It can't excuse behavior that contradicts a higher source or narrow what that source asks for.

Read the repository instructions that govern the touched files, such as `AGENTS.md` and `CONTRIBUTING.md`, the root `REVIEW.md` when the repository has one, the project's ADRs that cover the changed code, and the validation results. Existing review comments are leads; treat resolved or outdated threads as history.

If there are no requirements, review correctness against the code's evident purpose and report the missing context. Block approval only when a safe verdict is impossible without it.

Prepare the brief under **What every reviewer gets** in [REVIEWERS.md](REVIEWERS.md).

## 3. Choose reviewers

Choose the reviewers under **Lenses** in [REVIEWERS.md](REVIEWERS.md), and start them at the same time. Don't change the checkout while they run.

The reviewers must be independent of the change's author. If you wrote or changed the code under review, as when another skill built the PR in this conversation, start the reviewers as agents rather than reviewing it yourself. A reviewer that fails doesn't make this a host without agents, so don't replace it with a local pass. Standalone, a small change that you didn't write, such as a few files and a couple hundred changed lines, may be reviewed in one local pass per lens instead.

For adversarial, blind-spot, or tear-it-apart requests, start the reviewers as agents regardless of the change's size. First write one paragraph stating what the change is meant to accomplish, based on the sources in step 2, and mark what is inferred, and give every reviewer that paragraph. If the user wants the intent itself challenged, use the `relentless-review` skill for that separate question.

## 4. Check coverage

Wait for all reviewers, then compare each reviewer's inspected and skipped areas with the files its lenses should read. A lens may rule files out by stating why they fall outside it, as Security does for files that touch no trust boundary. Rerun a reviewer once if it failed, returned nothing, could not load a skill its lens uses, or skipped or left unmentioned files its lenses should read, limiting the rerun to what it missed. Report any gap that remains as a coverage gap, naming the lens and the files. A gap in a lens the **Correctness** verdict covers, as listed under **Report**, leaves the review incomplete, because nothing has checked those files for the harm that lens looks for.

A lens that says it has nothing to review, such as Security when the change touches no trust boundary, has returned a result. If no reviewer has returned a result after its rerun, the review failed: say so instead of reporting findings.

## 5. Check the findings

Treat reviewer output as leads; agreement between reviewers raises priority but doesn't prove a finding. Check each finding against the diff, the requirement or rule, whether the path is reachable, and the surrounding code, and plan to keep or drop it:

- Drop findings that are unsupported, already handled, settled by a user-approved requirement or decision that accepts the harm they name, preference-only, or enforced by tooling, and reasoned findings triggered by crafted or validation-rejected input unless the lens is Security. Also drop findings that predate the change; once the Verifier agrees, they go under **Noticed**.
- Keep a finding when a requirement asks for what causes its harm without accepting that harm, such as an issue asking reviewers to skip lockfiles where a swapped package then goes unread, and give a fix that meets both. When no fix can, keep it and name the requirement it conflicts with, so the person who set it can decide. An issue's background, survey, or examples settle nothing.
- Check the Noticed items reviewers return as under **Noticed problems** in [REVIEWERS.md](REVIEWERS.md).
- Merge duplicates and findings with a shared cause under the best-fitting lens. When you confirm a problem, check the rest of the diff for the same problem and report the locations together.

Then run the **Verifier** in [REVIEWERS.md](REVIEWERS.md), and keep each finding with the Outcome it settles on.

## Fix check

A calling skill runs this after it commits fixes for earlier findings and before it pushes them. It gives you, besides what every reviewer gets:

- the round's diff since the last reviewed commit, and every change since the first review. When those commits include a merge from the base branch, use `git log -p --no-merges <commit>..HEAD ^origin/<base>` instead of each diff, so the base branch's own changes stay out.
- the findings and comments the round addresses, each with the reply it drafted
- every earlier finding it rejected or accepted as a limit, with the reason

Start one reviewer with all of it. It applies the Correctness, Repository rules, and Scenarios lenses to the code the round adds, plus Security when that code touches a trust boundary, Blast radius when it alters a contract, and Rollout, Specification, or Tests when their condition matches. Ask it three questions:

1. Does each fix resolve its finding, as its drafted reply claims, on every path?
2. What does the round break? Look for a check moved after work it should guard, a fallible call before the step that schedules recovery, an early return that drops a result already computed, and a guarantee the code made before the round that it no longer makes. For a fix that changes validation, also look for any request, path, or value a legitimate caller could send that the code now rejects or newly accepts, beyond the input the finding names.
3. Which additions since the first review could shrink, merge into one fix at a shared cause, or be reverted, while still resolving the findings the round addresses? Give each one's net change in lines.

It reports every problem the round's code introduces or worsens. It doesn't raise points already settled by a rejection or an accepted limit, unless a later change to that code means the reason given no longer holds. Check its coverage and findings as in steps 4 and 5.

## Return to the caller

When another skill runs this review, return to it:

- the lenses that ran, each coverage gap with its lens and files, and whether the review is incomplete; or that the review failed
- whether reviewers ran as local passes instead of independent agents
- each path an agent changed in the checkout, the agent when its report names the change, and whether you undid it
- each kept finding with its lens, anchor, problem, trigger, Outcome, evidence, and fix, marked _(reproduced)_ when the evidence was reproduced, and whether the verifier confirmed it
- each dropped finding with its lens and the reason
- each finding left unverified or disputed, with your plan for it and each side's evidence
- any counterevidence you gave the verifier, quoting user decisions verbatim
- the Noticed items, written as under **Noticed items** and marking those left unverified

## Noticed items

Noticed items reach people who haven't read the code they're about, so write each one for a developer who has never opened that part of the codebase. Merge items that share a cause, keeping every location and the most harmful Outcome, and list the most harmful first. Write each in this shape:

```markdown
**What goes wrong, in plain words.** Who runs into it, when, and what they see. Then the cause, with the file and line, explaining any internal name the first time it appears.

- **Outcome:** a security hole, data loss, a crash, a stuck job, a wrong result, or a cost to future changes.
- **Why left:** why this change doesn't fix it, such as that it predates the change.
- **Next step:** the fix and its size, or the decision it needs first.
- **Evidence:** reproduced, with the probe or test, or reasoned, with the code path. For an unverified item, say what remains uncertain.
```

## Report

When a person asked for the review, open with a short summary of the change so the reader knows what it does before the verdicts. Write it for a developer who has not read the diff: two or three sentences in simple, everyday words, with technical terms only where they name something exactly, such as a file, command, or API. Describe what the change does and why, as its author intends it, without judging it.

Label each kept finding:

- **Must fix:** its Outcome is a security hole, data loss, a crash, a stuck job, or a wrong result; it breaks an applicable written rule; it is a structural problem with a named, significant cost to future changes; or it is a Tests finding that names a realistic regression in important behavior that would now go uncaught, through protection the change loses, a validation claim that doesn't hold, or changed behavior no test covers.
- **Suggestion:** a smaller problem whose fix has a concrete benefit you can name.

Set two verdicts. **Correctness** covers the Correctness, Diff read, Scenarios, Security, Blast radius, Rollout, Specification, and Tests findings, except Tests findings only about a test's maintenance cost. **Maintainability** covers the Repository rules and Simplicity findings, and those Tests findings. For each, take the first that applies:

- **Changes requested** if any must-fix finding remains; note missing information under Limitations
- **Blocked** if missing information, access, or a human decision makes approval unsafe, or a coverage gap or unanswered finding in a lens the verdict covers leaves the review incomplete
- **Approved** otherwise

No findings is a valid result. Do not add minor observations to fill the report.

A root `REVIEW.md` can shape this report but not shrink it. Put the opening it asks for, such as the number of findings, before **Change**, order findings within each section as it asks, and apply its limit on minor findings to Suggestions. Keep the verdicts and every section that has content, including Noticed and Limitations, even where it says to stop once there is nothing to fix.

Use this format and omit empty sections:

```markdown
**Change:** What the change does, and why, in two or three short sentences.

**Scope:** base..head (N commits), or working changes
**Correctness:** Approved | Changes requested | Blocked
**Maintainability:** Approved | Changes requested | Blocked

## Correctness

### Must fix: short title

`path/to/file.ts:42`. What happens, how this change causes it, and who is affected. The smallest fix.

## Maintainability

Same format as Correctness.

## Noticed

Problems the change doesn't cause, written as under **Noticed items**.

## Limitations

Coverage gaps, unverified or disputed findings, reviews done in local passes instead of by independent agents, changes an agent made to the checkout, and anything else that could not be checked, with whether it affects the verdict.

## Adversarial

Only for adversarial reviews: the intent tested, where reviewers disagreed, and dismissed leads worth a second look.
```

End by stating that the review made no changes.
