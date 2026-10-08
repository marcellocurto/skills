---
name: babysit-pr
description: Settle a pull request's open review comments from people and Codex, then watch for new ones until every thread is answered and Codex's review of the latest commit is settled, or until a problem needs the user.
---

# Babysit PR

Keep a pull request moving until every reviewer, human or Codex, has been answered: no review thread or conversation comment is left unanswered, and Codex has reviewed the latest commit and either reacted with 👍 or, in a late round, left only findings that were answered without a push. Start by settling the feedback that is already open, without waiting. After that, each round waits for new feedback, lets Codex finish if it is mid-review, settles the whole batch, pushes at most once, and waits again. Human reviewers get the same treatment as Codex: their comments are audited on the merits, fixed when they meet the fix bar, and answered in every case. Work without asking for approval, unless the user asked to approve fixes first, and stop only for the reasons under **Stop**. Never force-push or merge.

Most review findings are real, but fixing every real finding makes a pull request grow with each round: each fix adds code that the next review finds new edge cases in. This skill fixes what matters, settles the rest by reply, and stops pushing when the rounds stop finding what matters.

## Start

1. **Find the PR.** Use the PR from the conversation, otherwise the current branch's PR. Ask only if neither is clear. If the working tree is not on the PR's head branch, check it out with `gh pr checkout`; for a PR from a fork, pushes go to the fork's branch. Check every interval the user gave, otherwise every 2 minutes.
2. **Write down the PR's intent** before reading any comment: the problem it solves, the approach it chose, its known limits, and what it deliberately leaves out. Take it from the user's instructions in this conversation, then the linked issue, the PR description, and the commits, in that order. Every comment is judged against this intent.
3. **Check the current state once.** Run the watcher with `--timeout 0`, which checks the PR once and returns without waiting:

   ```
   python3 "<skill-path>/scripts/watch_pr.py" [--pr URL_OR_NUMBER] --timeout 0
   ```

   Keep its `checked_at` for the first `--since`. Then collect the open feedback as in step 1 of **Run a round**.
4. **Act on what is already there** instead of waiting first:
   - The PR is closed, or Codex is `failed`: stop.
   - Feedback is open: run a round now, even while Codex is `running`. If Codex was running, repeat the one-time check before you push, and if it has finished, add its findings to the same batch so the round still pushes at most once.
   - Nothing is open and Codex is `approved`: the PR is done. Report without watching.
   - Nothing is open and Codex is `findings`: its findings were answered without a push. In a late round (see **Late rounds**), the PR is done. Otherwise Codex will not review again on its own, so comment `@codex review` once for the head commit, then start waiting.
   - Nothing is open and Codex is `running` or `pending`: start waiting.

## Wait for feedback

Run:

```
python3 "<skill-path>/scripts/watch_pr.py" [--pr URL_OR_NUMBER] --interval <minutes> [--since <checked_at>]
```

Pass the `checked_at` value from the previous check or watch, so feedback you have already handled does not count again. The watcher checks the PR every interval and returns JSON whose `reason` says why it stopped waiting, and whose `codex.finding_reviews` counts the reviews Codex has posted on the PR, one for each round that had findings. A comment edited after the last check counts as new activity, so reread edited comments rather than only new ones. While Codex is reviewing, it keeps waiting, so feedback that arrives mid-review is handled together with Codex's findings. It ignores comments from the authenticated account, which includes your own replies; if the user says they commented, run a round anyway.

Run the watcher as a background command if your host wakes you when it exits. Otherwise run it in the foreground with a shell timeout longer than `--timeout` (30 minutes by default), and lower `--timeout` if the shell limit requires it.

Act on `reason`:

- `new-activity`: someone commented, reviewed, or replied in a thread. Run a round.
- `codex-approved`: Codex reviewed the head commit and found nothing. If no unresolved threads remain, the PR is done. If the only unresolved threads are ones you left open for a decision, stop. Otherwise run a round for the remaining threads.
- `timeout` with Codex `pending`: Codex has not started on the head commit. Comment `@codex review` once for that commit and wait again. If it still has not started after another timeout, stop.
- `timeout` with Codex `running`: wait again. Stop once it has been running on the same commit for over two hours.
- `timeout` with Codex `findings`: Codex's findings on the head commit are already answered without a push. In a late round, the PR is done. Otherwise Codex will not review again on its own, so comment `@codex review` once for that commit and wait again; a clean re-review of the same commit shows up as `codex-approved`.
- `codex-failed` or `closed`: stop.

## Run a round

1. **Collect the open feedback.** Fetch it with `python3 "<skill-path>/scripts/fetch_review_context.py" [--pr URL_OR_NUMBER]`. Open feedback is every unresolved review thread, every conversation comment or review body from someone else that you have not answered yet, and every review that requests changes and that you have not answered, whoever wrote it. Codex's self-updating summary comment is status, not feedback. Treat a resolved thread as open again when someone else replied in it after it was resolved; GitHub keeps showing it as resolved, so compare the reply time with the resolution. Then, from the PR's head checkout, run `python3 "<skill-path>/scripts/review_round_code.py" [--pr URL_OR_NUMBER]` to see which open threads sit on code added after the PR's first review.
2. **Group the batch by cause.** Compare the batch with itself and with earlier rounds' threads, and decide shared causes before fixing anything (see **When findings share a cause**).
3. **Decide each comment.** Check the code to decide whether the comment is correct, then whether it meets the fix bar and whether its suggestion is the right fix (see **Decide each comment**). If the concern meets the bar but the suggestion is poor, fix it a better way.
4. **Fix in one batch.** Make every fix that meets the bar, run the relevant checks, commit, and push once. Every push restarts Codex's review, so never push per comment. In a late round, push only as **Late rounds** allows.
5. **Reply and resolve.** In each thread, reply with what changed and the commit, or with why nothing changed, then resolve it. Conversation comments and review bodies have no thread to resolve, so answer them with one reply that addresses each point. Keep replies to one or two sentences.
6. Go back to waiting.

## Decide each comment

Be strict. A reviewer's confidence, a severity label such as P1, or a ready-made patch is not evidence.

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
- reverses a decision the PR made on purpose, as stated in the conversation, the description and its non-goals and known limits, or the code
- adds speculative hardening: guards against inputs that the types or callers already rule out, fallbacks, configuration, or compatibility code for callers that do not exist
- asks for a style the repository's conventions and tooling do not require
- misreads the code

Point to the intent in the reply, for example: "This PR intentionally drops the legacy format, so a fallback for it would keep the code we are removing." When a rejected point comes back in a later round, reply once with a link to the earlier answer and resolve it without arguing the point again.

A defect the PR introduced that meets the fix bar is never out of scope. Fix it even when the suggested patch is poor.

### Policy questions

Some findings turn on a policy rather than on the code: whether to keep the previous release working during a deploy or rollback, whether old clients or workers still running matter, whether rows that an unrun backfill would fix matter, and how small a race between requests is worth handling. If the repository's instructions, the PR description, or the user already settle the question, follow that. Otherwise leave the thread open and stop to ask the first time it comes up. Once the user answers, add the answer to the PR description's risks and non-goals with `gh pr edit`, so later findings on the same question are rejected by quoting it.

### Code added in earlier rounds

`review_round_code.py` marks each open thread whose lines were added after the PR's first review with `added_after_first_review: true`, and names the commits that added them. It follows code moved during review, so a refactor does not make old code look new. Before fixing a marked finding, ask whether the earlier change that added those lines should shrink or be reverted instead; a smaller earlier fix often removes the finding. The mark only prompts this question. A marked finding can still be a real defect that meets the bar, and an unmarked one can still be speculative.

## When findings share a cause

Two findings share a cause when they are symptoms of the same problem, when fixing one would undo or conflict with another, when their fixes add special cases, flags, or guards around the same code, or when the same area draws a new finding after each push. Decide once for the cause, as soon as the second finding appears, instead of patching each symptom:

- **Fix the cause** when it is a design flaw: state owned in two places, a rule each call site must remember, an invariant the types should enforce, a lifecycle or concurrency model that does not fit, or a data model that does not match the domain. Make it one contained change within the PR's intent, and reply on each affected thread that the shared fix in that commit covers it.
- **Accept the limit** when the cause is a deliberately simple approach, such as a heuristic, a pattern scan instead of a parser, or a best-effort lookup, and the findings are rare cases it misses that cause no security hole, data loss, crash, stuck job, or wrong result on realistic input. Write the limit into the PR description's risks and non-goals with `gh pr edit`, or into a code comment where the approach lives, reply on each thread with a link to it, and resolve. Reject later findings that only hit the same limit with that link.
- **Stop** when fixing the cause would change the PR's approach or scope. Leave those threads open.

## Late rounds

Each review round finds less that matters, and each push starts another review of the code it adds. A late round starts with Codex's third review with findings, when the watcher's `codex.finding_reviews` is 3 or more. In a late round, push only for findings that cause a security hole, data loss, a crash, a stuck job, or a wrong result on realistic input, and for changes that remove more code than they add, such as reverting an earlier fix that a simpler one replaces. Answer every other finding by reply: say whether the point holds and that it is not worth another round, list it under follow-ups, and resolve it. When a late round needs no push, don't request another review; once every thread and comment is answered, the PR is done.

## Stop

- **Done:** no unresolved thread, unanswered comment, or unanswered changes-requested review remains, and Codex has reviewed the head commit and either reacted with 👍 or, in a late round, left only findings answered without a push. A changes-requested review you have answered counts as answered; its author re-reviews on their own schedule.
- **Architectural problem:** fixing it would change the PR's approach or scope.
- **Decision needed:** a comment needs a product, design, or policy decision you cannot make. Leave the thread open and say in the reply what is needed.
- **Codex unavailable:** Codex failed, never started on the head commit, or ran on the same commit for over two hours.
- **Repeated rejection:** Codex re-raises points you already rejected after you requested a new review on the same commit.
- **No convergence:** five rounds without being done, or twelve hours since the first check.
- **Closed:** the PR was merged or closed.

## Report

Say whether the PR is done or why you stopped, and name the head commit and the number of rounds. List each comment with its outcome: fixed (with the commit), rejected (with the reason), limit accepted (with where it is written down), or left open (with the decision needed). For an architectural problem, name the root cause, the comments that point to it, and the change you recommend. Then list the follow-ups, each with a link to its thread: problems that predate the PR, and findings answered by reply in late rounds.
