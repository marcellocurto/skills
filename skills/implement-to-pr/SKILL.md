---
name: implement-to-pr
description: Implement a GitHub issue or the work agreed in the conversation, check it, and open a pull request that is ready for review.
---

# Implement to PR

1. Work out what to build. If you were given a GitHub issue, read it and its comments with `gh issue view <number> --comments`. Otherwise, build what we agreed on in this conversation. Don't add anything beyond that.
2. If you're on the main branch, create a new branch with a short name that describes the work. Leave unrelated local changes alone.
3. Build it the way the rest of the codebase does things, and follow the repository's instructions. Add or update tests where the change creates or alters behavior that users or callers rely on. When removing behavior, remove its tests rather than asserting its absence. While you build, keep checks narrow: lint and format only the files you changed, and run only the tests you wrote or that cover the code you changed. Save the full suites for the next step.
4. Once you think the work is complete, run the repository's full checks (formatting, linting, type checks, tests, and build) and read through the whole diff. If something fails, fix it using the same narrow checks, then run the full checks again. The work is done when everything the issue or conversation asked for works and every check passes. A check that already fails on the base branch for reasons unrelated to your change is not yours to fix; say so in the PR description instead of working around it. If a check needs a tool, runtime, or service that isn't installed here, such as a JDK, a database, or a browser, don't install system-level software without asking. Verify the change another way where you can, and report what didn't run in the PR description and your final response.
5. Commit, push, and open a pull request into the branch the user or repository instructions name, otherwise the default branch; `gh repo view --json defaultBranchRef` tells you which that is. Don't open it as a draft. Write the title and description as described below, save the description to a temporary file outside the repository, and pass it with `--body-file`.

If anything does not work as expected, don't hesitate to ask questions so we can get it working right. That includes an unclear request, a check that fails for a reason you can't find, and code that doesn't behave the way the issue assumes. Ask instead of guessing or working around the problem.

Never force-push or merge. When you're done, reply with the final response described below.

## Pull request title and description

Write both from the committed diff, the issue, and the check results. Use the conversation only for the decisions and rejected alternatives behind the change, and only where the diff reflects them. The readers are engineers who review many pull requests. Use simple, everyday words, with technical terms only where they name something exactly, such as a file, command, or API. Write short paragraphs, put the most important point first, and use backticks for code identifiers. Keep the description proportional to the change.

Title: the outcome in simple words that a reviewer understands without opening the PR, such as "Retry failed webhook deliveries with backoff" rather than "Update webhook logic".

Description, in this order:

```markdown
## Summary

Two to four sentences: what problem this solves, why it matters, and how behavior changes. A reader who stops here should know what the PR does. End with `Closes #N` when the PR fully resolves that issue in the same repository and targets the default branch, since GitHub closes linked issues only for those merges; otherwise reference it without closing it.

## Changes

The changes grouped by concern, each with the behavior before and after. Explain decisions a reviewer might question and the alternatives you rejected.

## How to review

Where to start, which parts need careful reading, and which are mechanical, such as renames, moved code, or generated files. Name any specific question you want the reviewer's judgment on.

## Verification

The commands run and their results, manual checks, and screenshots for UI changes. Say what was not tested and why, including each check that couldn't run because a tool or service is missing here, and what you did instead.

## Risks and non-goals

What could break, such as compatibility, migrations, performance, or security, and what this PR deliberately does not do.
```

Always include Summary and Verification. Include the other sections only when they have real content; a one-file fix usually needs only those two. Never write a section that says "None".

Leave out file-by-file change lists, restatements of the diff, unticked checkboxes, secrets, absolute local paths, and raw command output.

## Final response

This message is for the user, who already knows the request. Keep it short and point to the PR instead of repeating its description. Use these parts in this order, and leave out any part with nothing to say:

```markdown
**PR:** the link, and one sentence on what it does.

**Couldn't verify:** each check or tool that didn't run, what it would have caught, what you did instead, and what to install to run it. For example: "Java 25 isn't installed, so `./gradlew test` didn't run. I covered the parser with unit tests instead. Install Java 25 to run the full suite."

**Judgment calls:** assumptions and decisions the issue or conversation didn't settle, and anywhere the work differs from what was asked.

**Review focus:** the one to three places that need careful reading, and which parts are mechanical.

**Noticed, not done:** problems outside the scope that you found along the way.
```

Never say all checks pass when some didn't run. Name what passed and what didn't run.
