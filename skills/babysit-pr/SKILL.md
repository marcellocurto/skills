---
name: babysit-pr
description: Review a pull request with independent agents when it has no review yet, settle its open review comments from reviewers and people and its failing CI checks, and check each round of fixes with an independent reviewer before pushing, until every thread is answered and the required checks pass, or a problem needs the user.
---

# Babysit PR

Keep a pull request moving until every reviewer has been answered, the latest commit has been reviewed, and its required checks pass. The reviewers are independent agents this skill starts, as defined in [REVIEWERS.md](REVIEWERS.md), and people. The agents review the pull request once when it has no review yet, and check each round of fixes before it is pushed, so every pushed commit is reviewed without waiting for an outside service. Human reviewers get the same treatment as the agents: their comments are audited on the merits, fixed when they meet the fix bar, and answered in every case. A failing check is feedback too, decided under **Failing checks**. Work without asking for approval, unless the user asked to approve fixes first, and stop only for the reasons under **Stop**. Never force-push or merge.

Most review findings are real, but fixing every real finding makes a pull request grow with each round: each fix adds code that the next review finds new edge cases in. This skill fixes what matters, settles the rest by reply, and stops pushing when the rounds stop finding what matters.

## Start

1. **Find the PR.** Use the PR from the conversation, otherwise the current branch's PR. Ask only if neither is clear. If the working tree is not on the PR's head branch, check it out with `gh pr checkout`; for a PR from a fork, pushes go to the fork's branch.
2. **Write down the PR's intent** before reading any comment: the problem it solves, the approach it chose, its known limits, and what it deliberately leaves out. Take it from the user's instructions in this conversation, then the linked issue, the PR description, and the commits, in that order. Every comment is judged against this intent. Also note the requirements the reviewers get: the issue number, or the agreed request written out in full when there is no issue.
3. **Check the current state once.** Run the watcher with `--timeout 0`, which checks the PR once and returns without waiting:

   ```
   python3 "<skill-path>/scripts/watch_pr.py" [--pr URL_OR_NUMBER] --timeout 0
   ```

   Keep its `checked_at` for a later `--since`. Its `reviews` field gives `first_reviewed_commit`, `last_reviewed_commit`, and `fix_checks`; the head is reviewed when `last_reviewed_commit` equals `pull_request.head_sha`. Its `checks` field lists the head's `failing` and `pending` checks, each marked `required` when branch protection requires it, and `pull_request.mergeable` is `MERGEABLE`, `CONFLICTING`, or `UNKNOWN` while GitHub is still computing it.

4. **Act on what is there:**
   - The PR is closed: stop.
   - `first_reviewed_commit` is empty, or `last_reviewed_commit` is not an ancestor of the head because the branch was rebased: run the first review in [REVIEWERS.md](REVIEWERS.md) on the head commit, post it, and run the one-time check again.
   - Then collect the open feedback as in step 1 of **Run a round**. If any is open, run a round now.
   - Nothing is open and the head is not reviewed, because someone pushed commits after the last review: run a round to fix-check those commits.
   - Nothing is open, the head is reviewed, and `mergeable` is `CONFLICTING`: stop under **Conflict**.
   - Nothing is open, the head is reviewed, and a check is pending, `mergeable` is `UNKNOWN`, or the user asked you to wait for a person's review that hasn't arrived: wait for feedback.
   - Nothing is open, the head is reviewed, and a required check failed for a reason the PR didn't introduce: stop under **Checks fail outside the PR**.
   - Nothing is open and the head is reviewed: the PR is done. Report.

## Wait for feedback

The reviews this skill starts run inside the round, so there is nothing to wait for from them once every comment is answered. Wait when checks on the head are still running, when GitHub has not yet computed whether the PR conflicts with its base, or when the user asked you to wait for a person's review or gave an interval. Run:

```
python3 "<skill-path>/scripts/watch_pr.py" [--pr URL_OR_NUMBER] --interval <minutes> [--since <checked_at>]
```

Use the user's interval, otherwise 2 minutes. Pass the `checked_at` value from the previous check or watch, so feedback and check results you have already handled do not count again. The watcher checks the PR every interval and returns JSON whose `reason` says why it stopped waiting. A comment edited after the last check counts as new activity, so reread edited comments rather than only new ones. It ignores comments from the authenticated account, which includes your own replies and reviews; if the user says they commented, run a round anyway.

Run the watcher as a background command if your host wakes you when it exits. Otherwise run it in the foreground with a shell timeout longer than `--timeout` (30 minutes by default), and lower `--timeout` if the shell limit requires it.

Act on `reason`:

- `new-activity`: someone commented, reviewed, or replied in a thread. Run a round.
- `check-failed`: a check on the head failed. Run a round without waiting for the other checks.
- `checks-finished`: every check on the head has finished. Run the one-time check from **Start** and act on it.
- `conflict`: the PR conflicts with its base branch. Stop under **Conflict**.
- `timeout`: wait again, until the limit under **Stop**.
- `closed`: stop.

## Run a round

1. **Collect the open feedback.** If the PR's head on GitHub is ahead of your checkout, pull it first. Fetch the feedback with `python3 "<skill-path>/scripts/fetch_review_context.py" [--pr URL_OR_NUMBER]`. Open feedback is every unresolved review thread, every conversation comment or review body from someone else that you have not answered yet, every review that requests changes and that you have not answered, whoever wrote it, and every failing check on the head that you have not decided in an earlier round. Treat a resolved thread as open again when someone else replied in it after it was resolved; GitHub keeps showing it as resolved, so compare the reply time with the resolution. Then, from the PR's head checkout, run `python3 "<skill-path>/scripts/review_round_code.py" [--pr URL_OR_NUMBER]` to see which open threads sit on code added after the PR's first review.
2. **Group the batch by cause.** Compare the batch with itself and with earlier rounds' threads, and decide shared causes before fixing anything (see **When findings share a cause**).
3. **Decide each comment.** Check the code to decide whether the comment is correct, then whether it meets the fix bar and whether its suggestion is the right fix (see **Decide each comment**). If the concern meets the bar but the suggestion is poor, fix it a better way.
4. **Fix in one batch.** Make every fix that meets the bar, run the relevant checks, and commit. Draft the reply for each thread. In a late round, fix only what **Late rounds** allows.
5. **Check the fixes.** Run the fix check in [REVIEWERS.md](REVIEWERS.md) on every commit since `last_reviewed_commit`, which includes commits someone else pushed. Fix what survives your verification and commit. When those fixes change more than the lines a finding names, run the fix check once more on just those commits; if it still finds a problem that meets the bar, stop under **Fixes don't converge**. Skip this step when the round committed nothing and the head is reviewed.
6. **Push once,** then post the fix check's one-line review pinned to the pushed head. A round that settled every comment by reply and found no unreviewed commits pushes nothing and posts no fix check. A round that only fix-checked someone else's commits and needed no fix posts the review pinned to the current head.
7. **Reply and resolve.** In each thread, reply with what changed and the commit, or with why nothing changed, then resolve it. Conversation comments and review bodies have no thread to resolve, so answer them with one reply that addresses each point. Keep replies to one or two sentences. Failing checks get no reply; their outcomes go in the report.
8. Run the one-time check from **Start** again and act on it.

## Decide each comment

Be strict. A reviewer's confidence, a severity label, or a ready-made patch is not evidence.

### Fix bar

Fix a finding when the PR introduced the problem and either:

- it causes a security hole, data loss, a crash, a stuck job, or a wrong result on input that current users, data, or callers realistically produce; or
- the fix leaves the code no more complex: it adds no new state, flag, lock, version or generation field, schema field, dependency, or module.

When a real problem misses the bar, choose the cheapest response that handles it, in this order:

1. An operational step the reply can name, such as running a backfill, ordering a deploy, or draining old workers.
2. A simpler behavior that avoids the case, such as disabling a control while its request runs, or re-reading after a change instead of tracking which answer arrived last.
3. Accepting the limit, as under **When findings share a cause**.
4. Rejecting it as rare and recoverable. Say how rare it is and what recovers from it, such as the next poll, a reload, or a later check in the pipeline.

### Reject what works against the PR

Reply with the reason and resolve the thread when a comment:

- describes a problem the PR did not introduce because it already exists on the base branch. List it under follow-ups in the report. Never stop for a decision about it.
- asks for work outside the PR's intent, such as a new feature, an unrelated refactor, or a follow-up
- reverses a decision the PR made on purpose, as stated in the conversation, the description and its non-goals and known limits, the repository's instructions, or the code
- adds speculative hardening: guards against inputs that the types or callers already rule out, fallbacks, configuration, or compatibility code for callers that do not exist
- asks for a style the repository's conventions and tooling do not require
- misreads the code

Point to the intent in the reply, for example: "This PR intentionally drops the legacy format, so a fallback for it would keep the code we are removing." When a rejected point comes back in a later round, reply once with a link to the earlier answer and resolve it without arguing the point again.

A defect the PR introduced that meets the fix bar is never out of scope. Fix it even when the suggested patch is poor.

### Policy questions

Some findings turn on a policy rather than on the code: whether to keep the previous release working during a deploy or rollback, whether old clients or workers still running matter, whether rows that an unrun backfill would fix matter, and how small a race between requests is worth handling. If the repository's instructions, the PR description, or the user already settle the question, follow that. Otherwise leave the thread open and stop to ask the first time it comes up. Once the user answers, add the answer to the PR description's risks and non-goals with `gh pr edit`, so later findings on the same question are rejected by quoting it. When the answer will apply to later pull requests too, propose the line for the repository's instructions in the report.

### Code added in earlier rounds

`review_round_code.py` marks each open thread whose lines were added after the PR's first review with `added_after_first_review: true`, and names the commits that added them. It follows code moved during review, so a refactor does not make old code look new. Before fixing a marked finding, ask whether the earlier change that added those lines should shrink or be reverted instead; a smaller earlier fix often removes the finding. The mark only prompts this question. A marked finding can still be a real defect that meets the bar, and an unmarked one can still be speculative.

### Failing checks

Read the failed log before deciding. For a GitHub Actions check, take the run ID from the check's `url` and run `gh run view <run-id> --log-failed`; compare with the same check on the base branch's latest commit, from `gh run list --branch <base> --workflow <workflow>`. Then decide which case it is:

- **The PR caused it,** such as a test, type, or lint failure in code the PR touches: it is a finding the PR introduced, so fix it under the fix bar. A required check the PR broke always meets the bar, because the PR cannot merge until it passes.
- **Flaky or infrastructure,** such as a timeout, a runner or network error, or a test unrelated to the diff that passes on the base branch: rerun it once with `gh run rerun <run-id> --failed`. A check from another service can't be rerun this way, so treat it as failing outside the PR.
- **Already failing on the base branch** the same way: the PR did not introduce it, so list it under follow-ups instead of fixing it here.

A check that fails again after its rerun, for a cause the PR did not introduce, counts as failing outside the PR. When it is required, stop under **Checks fail outside the PR**.

## When findings share a cause

Two findings share a cause when they are symptoms of the same problem, when fixing one would undo or conflict with another, when their fixes add special cases, flags, or guards around the same code, or when the same area draws a new finding after each push. Decide once for the cause, as soon as the second finding appears, instead of patching each symptom:

- **Fix the cause** when it is a design flaw: state owned in two places, a rule each call site must remember, an invariant the types should enforce, a lifecycle or concurrency model that does not fit, or a data model that does not match the domain. Make it one contained change within the PR's intent, and reply on each affected thread that the shared fix in that commit covers it.
- **Accept the limit** when the cause is a deliberately simple approach, such as a heuristic, a pattern scan instead of a parser, or a best-effort lookup, and the findings are rare cases it misses that cause no security hole, data loss, crash, stuck job, or wrong result on realistic input. Write the limit into the PR description's risks and non-goals with `gh pr edit`, or into a code comment where the approach lives, reply on each thread with a link to it, and resolve. Reject later findings that only hit the same limit with that link.
- **Stop** when fixing the cause would change the PR's approach or scope. Leave those threads open.

## Late rounds

Each review round finds less that matters, and each push adds code for the next round to find edge cases in. A late round is any round after two fix checks, when the watcher's `fix_checks` is 2 or more. In a late round, push only for findings that cause a security hole, data loss, a crash, a stuck job, or a wrong result on realistic input, for failing checks the PR caused, and for changes that remove more code than they add, such as reverting an earlier fix that a simpler one replaces. Answer every other finding by reply: say whether the point holds and that it is not worth another round, list it under follow-ups, and resolve it.

## Stop

- **Done:** no unresolved thread, unanswered comment, or unanswered changes-requested review remains, the head commit has a first review or fix check pinned to it, no check on it is pending, every required check on it passed, and `mergeable` is `MERGEABLE`. A changes-requested review you have answered counts as answered; its author re-reviews on their own schedule.
- **Architectural problem:** fixing it would change the PR's approach or scope.
- **Decision needed:** a comment needs a product, design, or policy decision you cannot make. Leave the thread open and say in the reply what is needed.
- **Fixes don't converge:** the second fix check of a round still finds a problem that meets the bar. Don't push the round, and leave its threads open without replies. Report the problem, its cause, and the local commits left unpushed.
- **Conflict:** the PR conflicts with its base branch. Report that the base branch needs to be merged in and the conflicts resolved.
- **Checks fail outside the PR:** a required check fails for a cause the PR did not introduce, after one rerun or because it fails the same way on the base branch. Report the check, the lines of its log that show the cause, and why the PR did not cause it.
- **No convergence:** five rounds without being done, or twelve hours since the first check.
- **Closed:** the PR was merged or closed.

## Report

Say whether the PR is done or why you stopped, and name the head commit and the number of rounds. List each comment with its outcome: fixed (with the commit), rejected (with the reason), limit accepted (with where it is written down), or left open (with the decision needed). Label each first-review finding with its lens, and list the fix checks' findings with their outcomes too. List each failing check with its outcome: fixed (with the commit), passed after a rerun, or failing outside the PR (with the evidence). For an architectural problem, name the root cause, the comments that point to it, and the change you recommend. Then list the follow-ups, each with a link to its thread: problems that predate the PR, and findings answered by reply in late rounds. End with any policy answers worth adding to the repository's instructions, each as the line to add.
