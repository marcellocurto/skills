---
name: implement-to-pr
description: Implement a GitHub issue or the work agreed in the conversation, check it, and open a pull request that is ready for review. Use when the user asks to implement, build, or fix something and open a PR for it, or when another skill runs it. To also review the PR and settle its comments, use `ship-pr`.
---

# Implement to PR

While you work, leave problems outside the scope unfixed. Name a committed credential only by its file and line, never copying its value. When you start helper agents, ask each to also return the real problems it came across outside its task, with the file and line, who runs into each and when, what goes wrong and how badly, the fix with its size, and its evidence, following the same credential rule and without searching for more. Check every problem a helper agent returns against the code before you report it.

1. Work out what to build. If you were given a GitHub issue, read it and its comments with `gh issue view <number> --comments`. Otherwise, build what we agreed on in this conversation. Don't add anything beyond that.
2. If you're on the main branch, create a new branch with a short name that describes the work. Leave unrelated local changes alone.
3. Build it the way the rest of the codebase does things, and follow the repository's instructions. Add or update tests where the change creates or alters behavior that users or callers rely on. When removing behavior, remove its tests rather than asserting its absence. Read the project's ADRs that cover the code you change. If your change makes one false, update it in the same change, using the `domain-modeling` skill when available. Rewrite the ADR to state what the system now does, or delete it and fix the links to it when its decision no longer holds. Never mark it superseded unless the project documents a different way to revise ADRs. While you build, keep checks narrow: lint and format only the files you changed, and run only the tests you wrote or that cover the code you changed. Save the full suites for step 4.
4. Run the repository's full checks (formatting, linting, type checks, tests, and build) and read through the whole diff. If something fails, fix it using the same narrow checks, then run the full checks again. The work is done when everything the issue or conversation asked for works and every check passes, except a check that already fails on the base branch or can't run here. Before deciding that a check is one of those, read the **Verify** step of the `create-pull-request` skill and follow it, including how to confirm a base-branch failure and the rule against installing system-level software without asking. Don't work around those checks; note them for step 6 and the final response.
5. Check each changed flow end to end, the way the person or program that relies on it would use it: run the command, call the endpoint, or drive the interface in a browser, starting the app with the project's own commands. Passing tests don't replace this check. Record the scenario, the result you expected, the result you saw, and the command or interaction that showed it, and keep screenshots of interface changes. Compare interface changes with the project's design guidance, such as its design system or style guide. Without one, use the `frontend-design` skill when available, or otherwise compare them with the screens around them. If a flow fails, fix it, then run step 4's checks and this check again, so the record shows the final code. Note a flow that can't run here the way step 4 notes a check that can't. Skip this step only when the change has nothing a person or program can run, such as documentation or agent instructions, and say so.
6. Open the pull request with the `create-pull-request` skill, which commits, pushes, and writes the title and description. Give it the issue or agreed request, the decisions and rejected alternatives behind the change, and the results from steps 4 and 5, including each check that didn't run and why. When it opens or updates the PR, hold back its report; the final response below replaces it. When it stops without one, tell the user why and what's needed instead.

If anything does not work as expected, don't hesitate to ask questions so we can get it working right. That includes an unclear request, a check that fails for a reason you can't find, and code that doesn't behave the way the issue assumes. Ask instead of guessing or working around the problem.

Never merge. When you're done, reply with the final response described below.

## Final response

This message is for the user, who already knows the request. Keep it short and point to the PR instead of repeating its description. Use these parts in this order, and leave out any part with nothing to say:

```markdown
**PR:** the link, and one sentence on what it does.

**Screenshots:** for UI changes, the screenshots you took while checking, embedded as Markdown images with absolute local paths and a caption saying what each shows. They go here instead of in the PR.

**Couldn't verify:** each check or tool that didn't run, what it would have caught, what you did instead, and what to install to run it. For example: "Java 25 isn't installed, so `./gradlew test` didn't run. I covered the parser with unit tests instead. Install Java 25 to run the full suite."

**Judgment calls:** assumptions and decisions the issue or conversation didn't settle, and anywhere the work differs from what was asked.

**Review focus:** the one to three places that need careful reading, and which parts are mechanical.

**Noticed, not done:** real problems outside the scope that you or your helper agents came across, written and grouped as under **Noticed, not done** below.

**I'd fix now:**

1. What goes wrong and for whom, with the file and line. The fix and its size.

**Needs its own change or your decision:**

2. The same, ending with the size of the change or the decision it waits on.

**I'd leave:**

3. The problem in one sentence, and why it isn't worth doing.
```

Never say all checks pass when some didn't run. Name what passed and what didn't run.

### Noticed, not done

What the user decides about each item is whether to act on it. Write each one for a developer who has never opened that part of the codebase, as one or two plain sentences with no labelled fields: what goes wrong and for whom, with the file and line, then the fix and its size. When nothing goes wrong today, say which later change the problem makes harder or riskier. Explain an internal name the first time it appears.

Merge items that share a cause, keeping every location. Sort the items into the three groups by what you recommend, most harmful first within a group. Number them in one sequence across the groups, so the user can answer with the numbers, and leave out an empty group.

- **I'd fix now** holds only items whose fix is a few lines and needs no decision, and that you checked yourself: read the code and confirm what goes wrong, every place it happens, and that the fix is the size you say. Readers act on this group without looking again.
- An item you couldn't check that way goes in the second group and says what remains uncertain.
- An item whose fix is a new test goes under **I'd leave** unless the test would catch a realistic regression in behavior that users or callers rely on. An item whose fix is a shared helper goes there unless the helper would own a rule or concept; one that only builds a value or passes its arguments on doesn't.
