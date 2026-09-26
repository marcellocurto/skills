---
name: implement-to-pr
description: Implement a GitHub issue or the work agreed in the conversation, check it, and open a pull request that is ready for review.
disable-model-invocation: true
---

# Implement to PR

1. Work out what to build. If you were given a GitHub issue, read it and its comments with `gh issue view <number> --comments`. Otherwise, build what we agreed on in this conversation. Don't add anything beyond that.
2. If you're on the main branch, create a new branch with a short name that describes the work. Leave unrelated local changes alone.
3. Build it the way the rest of the codebase does things, and follow the repository's instructions. Add tests for any behavior you change.
4. Run the repository's usual checks (formatting, linting, type checks, tests, and build) and read through the whole diff. The work is done when everything the issue or conversation asked for works and every check passes.
5. Commit, push, and open a pull request into the main branch. That branch is usually `main` or `master`, and `gh repo view --json defaultBranchRef` tells you which. Don't open it as a draft. Give it a title that says what the change does. In the description, say what changed, why, and which checks you ran. If the PR finishes a GitHub issue, add `Closes #<number>`.

If anything does not work as expected, don't hesitate to ask questions so we can get it working right. That includes an unclear request, a check that fails for a reason you can't find, and code that doesn't behave the way the issue assumes. Ask instead of guessing or working around the problem.

When you're done, share the PR link. Never force-push or merge.
