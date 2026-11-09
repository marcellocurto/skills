# Reviews

`babysit-pr` runs the `code-review` skill for the first review of an unreviewed PR and for a fix check before each push. `code-review` decides whether each finding is real, what harm it causes, and whether the PR caused it; `babysit-pr` decides what to fix this round and publishes the results.

## What to give `code-review`

Give it the PR URL, the base branch, the head commit, the merge base, and what its brief asks for: the intent you recorded under **Start**, the user's decisions from this conversation, and the validation results. Tell it when this conversation built the PR, as `ship-pr` does, because you are then its author.

## First review

Run `code-review` as a review for another skill, pinned to the head commit. Don't push or change the checkout while it runs. If it reports that the review failed or is incomplete, stop under **Review failed or incomplete** in `SKILL.md`.

Apply [Decide each comment](SKILL.md#decide-each-comment) to its findings. Post as threads:

- each kept finding that meets the fix bar, including unverified ones `code-review` planned to keep
- each disputed finding, and each unverified finding `code-review` planned to drop, so a round settles it in public. The exception is a security finding that may describe code already on the base branch: keep it off GitHub and list it in the report as unsettled, because posting it would disclose a live vulnerability.

For a real finding below the bar, choose its response under **Fix bar** and list it in the report instead of posting it.

Post the threads as one review pinned to the reviewed head, with an inline thread per finding. Use `COMMENT`; authors cannot approve or request changes on their own PR.

Start each inline comment with the lens and a short title in bold, followed by _(reproduced)_ when the evidence was reproduced. Then give the problem, its trigger if it has one, and the fix in two to four sentences. Link each cited rule and any affected code outside the diff with a full-SHA permalink, such as `https://<host>/<owner>/<repo>/blob/<full-sha>/src/a.ts#L10-L14`, pinned to the reviewed head commit, or to the merge base for a rule the diff edits. The review body is one line naming the lenses that ran, such as "Reviewed `abc1234` for correctness, repository rules, scenarios, simplicity, security, blast radius, and diff read: 3 findings, inline." Leave out a lens that never returned a result. When a lens left a coverage gap, end the line with it, such as "Security did not cover `src/a.ts`." When no finding is posted, post the review with only that line, with its count reading "nothing to change." `watch_pr.py` recognizes the first review by the body's opening "Reviewed \`", so keep that wording.

With `gh`, write the review to a JSON file outside the repository and post it:

```
gh api --hostname <host> repos/<owner>/<repo>/pulls/<number>/reviews --method POST --input <file>
```

```json
{
  "commit_id": "<head-sha>",
  "event": "COMMENT",
  "body": "Reviewed `abc1234` for correctness, repository rules, simplicity, security, blast radius, and diff read: 2 findings, inline.",
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

An out-of-diff anchor rejects the whole review. Move it to a causal changed line in the same file and retry. Read back the review to confirm every comment posted once; check existing reviews before retrying an uncertain post.

## Fix check

After a round's fixes are committed and before they are pushed, run `code-review` as a fix check, with the inputs its **Fix check** section lists. Take `last_reviewed_commit` and `first_reviewed_commit` from the `reviews` field of `watch_pr.py`; a round's second fix check starts at the commit the first check reviewed. What the round answers is its threads and the fix-check findings it fixes, each with the reply you drafted.

If it reports that the review failed or is incomplete, stop under **Review failed or incomplete** in `SKILL.md`. If a finding stays disputed, or is unverified when `code-review` planned to drop it, stop under **Reviewers disagree**. Otherwise apply [Decide each comment](SKILL.md#decide-each-comment), including **Late rounds**, to its findings. Its findings don't become threads. Fix the ones that qualify in the same push, and list the rest under follow-ups with the reason another round is unwarranted.

After the push, post a review with no inline comments, pinned to the pushed head, whose body is one line such as "Reviewed the fixes in `abc1234`: 2 findings fixed before this push." or "Reviewed the fixes in `abc1234`: nothing to change." When it left a coverage gap, end the line with it, such as "Security did not cover `src/a.ts`." `watch_pr.py` counts fix checks and recognizes a reviewed head by that opening, so keep the wording.

## Noticed problems

`code-review` returns Noticed items: problems the PR neither introduces nor worsens, including first-review security findings dropped because they predate it. Keep them for the report. They get no fix in this PR and never block it.

Don't post them on GitHub, in review bodies or anywhere else, because a public comment about an unfixed security problem discloses it.
