---
name: implement-to-pr
description: Implement a GitHub issue or the work agreed in the conversation, check it, and open a pull request that is ready for review. Use when the user asks to implement, build, or fix something and open a PR for it, or when another skill runs it. To also review the PR and settle its comments, use `ship-pr`.
---

# Implement to PR

1. Work out what to build. If you were given a GitHub issue, read it and its comments with `gh issue view <number> --comments`. Otherwise, build what we agreed on in this conversation. Don't add anything beyond that.
2. If you're on the main branch, create a new branch with a short name that describes the work. Leave unrelated local changes alone.
3. Build it the way the rest of the codebase does things, and follow the repository's instructions. Add or update tests where the change creates or alters behavior that users or callers rely on. When removing behavior, remove its tests rather than asserting its absence. While you build, keep checks narrow: lint and format only the files you changed, and run only the tests you wrote or that cover the code you changed. Save the full suites for step 5.
4. Once you think the work is complete, simplify it. Use the `audit-code-complexity` skill when available: name your changes against the base branch, including uncommitted work, as the change to audit, and ask it to apply its findings. Without it, read the diff for code no requirement needs, wrappers that only forward a call, the same rule kept in more than one place, and guards for cases that can't happen, and simplify what you find. Leave anything that would change behavior or what was agreed as it is, and name it under **Judgment calls** in the final response.
5. Run the repository's full checks (formatting, linting, type checks, tests, and build) and read through the whole diff. If something fails, fix it using the same narrow checks, then run the full checks again. The work is done when everything the issue or conversation asked for works and every check passes, except a check that already fails on the base branch or can't run here. Before deciding that a check is one of those, read the **Verify** step of the `create-pull-request` skill and follow it, including how to confirm a base-branch failure and the rule against installing software. Don't work around those checks; note them for step 6 and the final response.
6. Open the pull request with the `create-pull-request` skill, which commits, pushes, and writes the title and description. Give it the issue or agreed request, the decisions and rejected alternatives behind the change, and the results from step 5, including each check that didn't run and why. When it opens or updates the PR, hold back its report; the final response below replaces it. When it stops without one, tell the user why and what's needed instead.

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

**Noticed, not done:** problems outside the scope that you found along the way.
```

Never say all checks pass when some didn't run. Name what passed and what didn't run.
