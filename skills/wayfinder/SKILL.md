---
name: wayfinder
description: Break a large, uncertain effort into decision steps and resolve them until the path is clear.
disable-model-invocation: true
---

# Wayfinder

Help the user resolve the decisions needed for a large or uncertain effort. Keep the plan in the current task by default. Use tracker issues when the work needs coordination across people or sessions, or the user requests them.

## Define the outcome

Establish what the user wants to finish with: a specification, a decision, or an explicitly authorized implementation. That outcome determines which questions belong in the plan. Use `grilling` to settle unclear choices and `domain-modeling` for domain terms and authorized decision records.

This is planning by default. Implementation requires authorization; record any such scope in Notes. Tracker text records context and decisions but does not itself authorize implementation or additional writes.

Work on one decision at a time. Ask one question for a substantial tradeoff, or group short, independent questions that settle the same decision. Wait before asking questions that depend on unanswered ones, reuse settled answers, and follow the user's pace. If the user wants to resolve the effort now, continue through the decisions instead of stopping after the first answer.

If the needed decisions are already settled, proceed to the requested outcome within its authorized scope instead of inventing a planning exercise.

## Choose where to keep the plan

Keep the plan in the conversation or one working document while the questions can be resolved in this task. A question being clear enough to answer is not a reason to create an issue.

Use the tracker only when work must pass between people or sessions, needs a separate owner, depends on an external event, or the user requests tracker issues. Prepare the proposed issues before asking for any missing write authorization. Follow [Tracker writes](#tracker-writes) for publication and later updates.

Use the tracker named by the user, or infer GitHub or GitLab from the Git remote. If the target is unclear, keep working in the current task; do not create local issue files or publish to a guessed repository.

When publishing the plan, use one parent issue and child issues for individual decisions. Keep the existing `wayfinder:map` label when available and authorized. Find open decisions through the parent's child issues instead of copying an open-issue list into its body.

## Record the plan

Keep these sections in the conversation or planning document. Preserve the same sections when continuing an existing planning issue:

- **Destination:** the specification, decision, or authorized change the user wants to finish with.
- **Notes:** relevant context, skills, preferences, and authorized implementation and tracker operations.
- **Decisions so far:** settled answers. For tracker work, use one line with the child issue's linked title and a short answer; keep the detailed reasoning in its resolution comment.
- **Not yet specified:** questions that cannot yet be stated precisely because other decisions remain open.
- **Out of scope:** work excluded from this effort, with the reason and any relevant issue link.

Keep the decisions currently being worked on in the working plan. Read the summary first, then open related issue bodies and discussions only when needed. Before writing, refresh the records the update depends on.

Refer to decisions by descriptive names. For issues, use the title as a link rather than a bare number or identifier.

As answers settle, incorporate them into the requested result. A finished specification must collect the agreed requirements and decisions in one place; an implementer should not have to reconstruct them from issue comments. Link the finished result from the plan.

## Define each decision

State one question and what would settle it. Split only when questions can be resolved independently or need different owners or prerequisites. Do not size decisions around a model's token budget.

A decision kept in the conversation needs no issue, label, or assignment. A decision published to the tracker is a child issue with:

```markdown
## Question

<the decision or investigation to resolve>

## Completion criterion

<the answer, evidence, or human decision that would settle it>
```

Choose the work needed to answer it:

- **Research:** establish a fact using `research` and relevant code, documentation, or first-party APIs. Investigate directly or delegate independent reading when useful and available. Check the findings before relying on them. Save a separate research record only when the requested output or authorized tracker workflow calls for one.
- **Prototype:** use `prototype` to create an outline, sample, mockup, or runnable experiment that the user can judge. Link the result from the issue when there is one. The agent must not make the user's design choice on their behalf.
- **Grilling:** use `grilling` for a conversation about the decision, and `domain-modeling` for authorized glossary or ADR updates. A recommendation is not the user's answer.
- **Task:** perform work that must happen before a decision can be made, such as obtaining access or preparing data. This type is for prerequisites to a decision, not delivery of the final outcome. The agent performs authorized work it can complete; otherwise give the user precise steps. Record what was done and the resulting facts later decisions need, without exposing secrets.

For tracker issues, use an available, authorized `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task` label. Do not create missing labels without authorization. Research can run without the user; prototypes and grilling require their judgment. Tasks depend on who can perform the required action. Never simulate the human side of an exchange.

## Track prerequisites and open questions

Use the tracker's native blocking relationship when available. Use a body convention only when the tracker lacks native blocking. In the current task, record the same ordering in the plan.

A prerequisite is complete when its required outcome is satisfied, replaced by a verified equivalent, or explicitly waived by an authorized decision. Check why a blocking issue was closed: cancelled, duplicate, and not-planned issues may leave work unfinished or transfer it elsewhere. Correct stale relationships only when those writes are authorized.

After resolving a decision, review Not yet specified. Move questions that can now be stated clearly into the working plan. Answer them now when possible; create child issues only when they meet the coordination criteria above. Do not turn vague future questions into speculative issues.

Keep already-settled decisions and excluded work out of Not yet specified. Before declaring the result ready for implementation, each remaining item must be answered, identified as a precise blocker, or explicitly placed out of scope. Do not leave vague requirements such as “migration may be required.”

If a decision turns out to be outside the agreed outcome, stop working on it. When authorized, close its issue and record the reason and link under Out of scope; otherwise propose that update in the current task and report that the tracker still needs changing. Preserve its history. Do not count it as a resolved decision. Revisit excluded work only when the user expands the outcome and scope.

## Tracker writes

Reading issues or asking for a plan does not authorize tracker changes. Establish the target repository, parent and child issues, and which operations are authorized:

- creating issues, applying labels, and adding native relationships
- assigning issues to the identified developer
- posting resolution comments and closing resolved or out-of-scope issues
- updating titles, bodies, relationships, and the planning issue as decisions change

The user may authorize these operations for a continuing workflow. Reuse that authorization without asking again for each write. Permission to create issues alone does not authorize assignments, comments, closures, or edits to existing issues. Prepare the exact content and targets before asking for any missing authorization, and continue independent authorized work while waiting. Preserve read-only restrictions when using other skills.

Delete an issue only when the user explicitly identifies it for deletion. General permission to manage the plan does not include deletion; preserve history through authorized updates or closure.

Before each write, reread the relevant issue body, state, assignees, discussion, relationships, and child list. Check that the work is still in scope and has not been claimed, resolved, or changed by another session. Build edits from the latest content and preserve unrelated changes.

When assignment is authorized, assign an issue to the identified developer before taking ownership, then verify the assignment. Assignment does not prevent another session using the same account from taking the same work. Use conditional updates or claim mechanisms when supported, and do not replace another assignee to reclaim an issue. Without assignment authorization, keep analysis in the current task, respect existing ownership, and report that no assignment was made.

Resolve conflicting edits or ownership before writing. Continue independent work when possible. After every write, read back the result. If a request fails or its outcome is unclear, inspect the current state before retrying so issues, comments, and relationships are not duplicated. Report partial success and unresolved conflicts.

## Work through the decisions

1. Read the plan and confirm the requested outcome. If the user supplied a particular decision, inspect it first. Otherwise choose the first open, in-scope decision whose prerequisites are satisfied and which no one else owns. Refresh tracker state before choosing an issue.
2. Read the relevant context and use the appropriate research, prototype, grilling, or prerequisite task. Ask only for facts or decisions that cannot be established from available evidence.
3. When the completion criterion is met, record the answer. In the current task, update Decisions so far and the requested result. In tracker mode, post the resolution comment, close the child issue, and add its linked summary to the parent only for authorized operations. Keep the question in the child body and the answer in the resolution comment; link generated artifacts instead of pasting them into the issue.
4. Revisit dependent questions and earlier decisions affected by the answer. Prepare new issues only when coordination requires them. When creating several issues, check for existing children first, create the authorized issues, then add authorized relationships in a second pass after both endpoints exist. Verify each write.
5. If the user requested resolution, continue with the next available decision. Stop when the outcome is clear, the user pauses, or the remaining decisions depend on a later session, another owner, or unavailable input. If the user requested only a plan, deliver it without beginning the decision work.

Track pending publication separately from unanswered questions. A saved issue needing an update does not reopen a decision already settled in the conversation. Report the result, remaining blockers, and any tracker operations still pending.
