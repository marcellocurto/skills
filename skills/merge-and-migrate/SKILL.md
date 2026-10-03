---
name: merge-and-migrate
description: Merge pull requests into the main branch in dependency order, promote it through each deployment branch with pull requests, and run pending migrations at the correct point for each environment.
disable-model-invocation: true
---

# Merge and Migrate

Ship the requested pull requests: merge them into the main branch, promote that branch through every environment in order, and run each pending migration at the point where the code and the data stay compatible. The repository may have no environment branches or several, and migrations may target any system, such as a SQL database, Convex, a search index, or a queue. Learn how this repository does it instead of assuming. The user's request authorizes every merge and every in-scope migration, including production, so work without asking for approval and stop only for the reasons under **Stop**. Never force-push, and never bypass branch protection with an admin override.

## Map the release setup

Before changing anything, work out how this repository releases. Read the repository's agent instructions and README, the CI and deploy workflows, the package scripts, the migration tool's directory and configuration, and the git history of the environment branches. Write down:

- **Main branch:** the branch the user named, otherwise the default branch from `gh repo view --json defaultBranchRef`.
- **Environments in order:** each environment, the branch that deploys it, and what triggers the deploy. The main branch may deploy an environment itself, and a repository with only a main branch has at most one environment.
- **Promotion route:** how earlier promotions moved changes, such as `main` into `dev` and `main` into `prod`, or `main` into `dev` and then `dev` into `prod`, and which merge method they used. Merge commits like "Merge main into dev" in the environment branches show this.
- **Migrations:** where they live, the command that applies them in each environment, the command that shows what is already applied, whether the tool has a dry run, and whether a deploy applies them on its own.
- **Deploy status:** where to see that a deploy finished, such as workflow runs, commit statuses, or GitHub deployments.

If any part of the release path stays unclear after reading, stop and ask instead of guessing.

## Work out what ships

1. **Pull requests.** Take them from the user's request. Fetch each with `gh pr view` to learn its base branch, head commit, checks, and mergeability.
2. **Extra commits.** Commits already on the main branch that are not yet in an environment branch ship too. That is expected; list them in the report.
3. **Environment-only commits.** For each environment branch, list the commits that are not on the main branch, ignoring merge commits, for example a hotfix pushed straight to `prod`. Leave them where they are; the forward promotion keeps them, and the report names them.
4. **Pending migrations per environment.** Compare each environment branch with the main branch after the requested pull requests, and collect every migration in that difference, not only the ones in the named pull requests. Then check each environment's applied state so you skip migrations that already ran there.

## Plan the order

**Pull requests.** Merge a stacked pull request after the one it is based on, and a pull request after any other that it needs code or migrations from. When nothing links them, keep the order the user gave.

**Migrations.** Decide for each migration whether it runs before or after the deploy of the code that ships with it:

- **Before the deploy** when the new code depends on what the migration creates, such as a table, column, index, or field.
- **After the deploy** when the migration needs the new code, as data migrations written as application functions do, or when it removes or narrows something the old code still uses.
- **Across two deploys** when neither order keeps both the running code and the stored data valid, for example a schema change that existing rows would violate until a backfill runs. Stop and explain the sequence it needs.

When the project documents its own procedure, follow it. Keep the tool's own migration order. If migrations from different pull requests claim the same sequence position or depend on each other in the opposite order, stop.

Every merge into a branch that deploys an environment is a deploy. When the main branch deploys an environment, the merges in the next section are that environment's deploys, so run its before-deploy migrations for a pull request before merging it.

## Merge the pull requests

For each pull request, in the planned order:

1. If it is stacked on a pull request you just merged, retarget it to the main branch with `gh pr edit --base` when GitHub has not done so.
2. If the repository requires branches to be up to date, update it with `gh pr update-branch`.
3. Wait until its required checks pass and it is mergeable. Resolve conflicts that are purely mechanical; stop on conflicts that change behavior.
4. Merge it with `gh pr merge` using a method the repository allows, preferring the one its history uses. Missing approval is not a reason to wait, but a merge blocked by branch protection is a reason to stop.

After the last merge, record the head of the main branch as the **release commit**. Every environment receives this commit.

## Promote each environment

Promote through pull requests. Open a pull request from the promotion source into the environment branch and merge it, instead of merging locally and pushing. Branch protection often blocks direct pushes, and the pull request runs the branch's checks and records what was promoted. Push directly only when the repository's instructions say promotions work that way.

For each environment, in order:

1. **Confirm the previous environment.** Start only after the previous environment's deploy and migrations succeeded and checked out.
2. **Run before-deploy migrations** for this environment, with a dry run or status check first when the tool has one.
3. **Open the promotion pull request** into the environment branch, titled like "Promote main to prod". Its head must be the release commit, or the previous environment's branch when that is the promotion route. If the main branch has moved past the release commit, open it from a temporary branch created at the release commit, and delete that branch after merging. List the shipped pull requests and the pending migrations in its description.
4. **Merge it** once its checks pass, with a merge commit unless earlier promotions used another method, so the environment branch keeps the main branch's history.
5. **Wait for the deploy** to finish and succeed.
6. **Run after-deploy migrations** for this environment. When the deploy applies migrations on its own, check their result instead of running them again.
7. **Verify.** Confirm each migration's effect with its audit or status output, a count of the affected records, or a smoke check of the deployed app.

Run each migration with the project's command and that environment's own configuration. Never point one environment's command at another environment's data by editing configuration files. Never retry a failed migration or roll anything back on your own.

## Stop

Stop and report when:

- the release path, a promotion route, or a migration command stays unclear after reading the repository
- a pull request's checks fail, it conflicts in a way that changes behavior, or branch protection blocks its merge
- a migration needs a sequence across two deploys, or migrations conflict in order
- a migration would delete or rewrite data in a way that neither the pull request nor the user's request describes
- a deploy fails, a migration fails, or verification shows anything unexpected
- the credentials or access for an environment are missing; name the exact command the user needs to run

Never continue to the next environment after a stop.

## Report

Say whether everything shipped or where you stopped and why. Then list:

- each merged pull request with its merge commit
- the extra commits from the main branch that shipped with them
- the release commit
- for each environment: the promotion pull request, the deploy result, each migration with whether it ran before or after the deploy, how it was verified, and its result
- the environment-only commits found on each environment branch
- anything left undone, with the command or decision needed to finish it
