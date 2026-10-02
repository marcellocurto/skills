---
name: pr-comments-audit
description: Audit open pull-request comments, fix and push the justified ones, and reply to and resolve each thread.
---

# PR Comments Audit

Settle the open comments on a pull request. Run the whole workflow without asking for approval, unless the user asked to approve the audit first.

1. **Find the PR.** Use the PR from the conversation, otherwise the current branch's PR. Ask only if neither is clear. If the working tree is not on the PR's head branch, check it out with `gh pr checkout`; for a PR from a fork, pushes go to the fork's branch. Fetch its comments with `python3 "<skill-path>/scripts/fetch_review_context.py" [--pr URL_OR_NUMBER]`. The script returns everything, so select the open feedback yourself: every unresolved review thread, every conversation comment or review body from someone else that you have not answered, and every review that requests changes that you have not answered.
2. **Audit each open comment.** Check the code to decide whether the comment is correct and whether its suggestion is the right fix. A reviewer's confidence or a ready-made patch is not evidence. If the concern is real but the suggestion is poor, fix it a better way.
3. **Fix.** Make the justified fixes, run the relevant checks, commit, and push to the PR branch. Reply in each thread with what changed and the commit, then resolve it.
4. **Explain.** For comments that need no fix, reply with the reason, then resolve the thread. Conversation comments and review bodies have no thread to resolve; a reply settles them.
5. **Leave open** only comments that need a decision you cannot make, and say in the reply what is needed.

Finish with a short list of each comment and its outcome. Never force-push or merge.
