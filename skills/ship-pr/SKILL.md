---
name: ship-pr
description: Implement a GitHub issue or the work agreed in the conversation as a pull request, then review it with independent agents, settle every review comment, and check each round of fixes before it is pushed. Use when the user asks to ship an issue or change end to end, or to build it and then babysit the PR. To only open the PR, use `implement-to-pr`.
---

# Ship PR

Take work from request to a settled pull request in two stages: build it and open the PR, then babysit it. This skill runs the `implement-to-pr` and `babysit-pr` skills in sequence. `babysit-pr` reviews the new PR with independent agents, settles every comment, and checks each round of fixes before pushing it. Never force-push or merge.

## 1. Build and open the PR

Follow the `implement-to-pr` skill through opening the pull request. Hold back its final response; its parts go into the report at the end. If it stops to ask the user something, this skill waits for the answer too.

## 2. Babysit

Run the `babysit-pr` skill on the new PR. Give it the requirements: the issue number, or the agreed request written out in full when there is no issue. The PR has no review yet, so `babysit-pr` starts with its first review, which gives the reviewers nothing from the implementation conversation, and then settles the findings and any comments from people.

## Report

When `babysit-pr` finishes or stops, send one message that combines the final response from `implement-to-pr` with the report from `babysit-pr`. Use these parts in this order, and leave out any part with nothing to say:

```markdown
**PR:** the link, and one sentence on what it does.

**Status:** done, or why babysitting stopped, with the head commit and the number of rounds.

**Screenshots:** for UI changes, the screenshots taken while checking, embedded as Markdown images with absolute local paths and a caption saying what each shows. When a fix changed the UI, show the version at the head commit.

**Couldn't verify:** each check or tool that didn't run, what it would have caught, what you did instead, and what to install to run it.

**Judgment calls:** assumptions and decisions the issue or conversation didn't settle, and anywhere the work differs from what was asked.

**Review focus:** the one to three places in the final diff that need careful reading, and which parts are mechanical.

**Feedback:** each review finding, labeled with its lens, each fix-check finding, and each human comment, with its outcome: fixed (with the commit), rejected (with the reason), limit accepted (with where it is written down), or left open (with the decision needed). For an architectural problem, name the root cause and the change you recommend.

**Noticed, not done:** problems outside the scope that you found along the way, `babysit-pr`'s follow-ups, and the policy lines it proposes for the repository's instructions.
```

Never say all checks pass when some didn't run. Name what passed and what didn't run.
