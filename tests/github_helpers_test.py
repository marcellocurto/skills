"""Offline behavioral checks for the independently installed GitHub helpers."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_helper(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REVIEW_HELPERS = [
    load_helper(f"review_{name.replace('-', '_')}", f"skills/{name}/scripts/fetch_review_context.py")
    for name in ("babysit-pr", "to-tickets")
]
RELATIONSHIPS = load_helper("relationships", "skills/to-tickets/scripts/set_issue_relationship.py")
# The watcher imports its sibling helper the way it does when run as a script.
sys.path.insert(0, str(ROOT / "skills/babysit-pr/scripts"))
WATCHER = load_helper("watch_pr", "skills/babysit-pr/scripts/watch_pr.py")


class OfflineTest(unittest.TestCase):
    def setUp(self):
        # A missed mock must fail instead of invoking a real CLI or making a write.
        self.process_guard = patch("subprocess.run", side_effect=AssertionError("Unexpected subprocess"))
        self.process_guard.start()
        self.addCleanup(self.process_guard.stop)


class ReviewTargetTests(OfflineTest):
    def test_explicit_urls_preserve_host_and_accept_fragments(self):
        cases = [
            (None, "https://github.com/acme/app/pull/7#discussion_r123", "github.com"),
            (None, "https://git.acme.test/acme/app/pull/7/files?diff=split#r123", "git.acme.test"),
            ("acme/app", "https://git.acme.test/acme/app/pull/7", "git.acme.test"),
            ("git.acme.test/acme/app", "https://git.acme.test/acme/app/pull/7", "git.acme.test"),
        ]
        for module in REVIEW_HELPERS:
            for repo, url, host in cases:
                with self.subTest(helper=module.__name__, repo=repo, url=url):
                    with patch.dict("os.environ", {"GH_HOST": "unrelated.test"}):
                        target = module.resolve_pr(repo, url)
                    self.assertEqual((target.host, target.owner, target.repo, target.number),
                                     (host, "acme", "app", 7))

    def test_conflicting_repository_or_host_is_rejected(self):
        for module in REVIEW_HELPERS:
            for repo in ("github.com/acme/app", "acme/other"):
                with self.subTest(helper=module.__name__, repo=repo):
                    with self.assertRaisesRegex(ValueError, "does not match"):
                        module.resolve_pr(repo, "https://git.acme.test/acme/app/pull/7")

    def test_number_uses_explicit_or_environment_host(self):
        for module in REVIEW_HELPERS:
            with self.subTest(helper=module.__name__):
                with patch.dict("os.environ", {"GH_HOST": "git.acme.test"}):
                    self.assertEqual(module.resolve_pr("acme/app", "7").host, "git.acme.test")
                    self.assertEqual(module.resolve_pr("github.com/acme/app", "7").host, "github.com")
                with patch.dict("os.environ", {"GH_HOST": ""}):
                    self.assertEqual(module.resolve_pr("acme/app", "7").host, "github.com")

    def test_checkout_resolution_keeps_host_from_cli_url(self):
        for module in REVIEW_HELPERS:
            for pr, payload in [("7", {"url": "https://git.acme.test/acme/app"}),
                                (None, {"url": "https://git.acme.test/acme/app/pull/7"})]:
                with self.subTest(helper=module.__name__, pr=pr):
                    with patch.object(module, "run", return_value=json.dumps(payload)):
                        target = module.resolve_pr(None, pr)
                    self.assertEqual((target.host, target.number), ("git.acme.test", 7))

    def test_authentication_failure_names_only_the_target_host(self):
        for module in REVIEW_HELPERS:
            with self.subTest(helper=module.__name__):
                with patch.object(module, "run", side_effect=RuntimeError("expired credential")) as run:
                    with self.assertRaisesRegex(RuntimeError, "login --hostname git.acme.test"):
                        module.ensure_authenticated("git.acme.test")
                run.assert_called_once_with(
                    ["gh", "auth", "status", "--active", "--hostname", "git.acme.test"]
                )


def connection(nodes, cursor=None):
    return {"nodes": nodes, "pageInfo": {"hasNextPage": cursor is not None, "endCursor": cursor}}


class ReviewPaginationTests(OfflineTest):
    def test_cli_fetches_outer_pages_and_each_threads_remaining_comments(self):
        for module in REVIEW_HELPERS:
            with self.subTest(helper=module.__name__):
                requests = []

                def fake_run(command, stdin=None):
                    self.assertIn("--hostname", command)
                    self.assertEqual(command[command.index("--hostname") + 1], "git.acme.test")
                    if command[1:3] == ["auth", "status"]:
                        self.assertIn("--active", command)
                        return "Authenticated"
                    self.assertEqual(command[1:3], ["api", "graphql"])
                    # Strings travel as raw `-f` fields so a digit-only owner stays a string;
                    # only the number is typed with `-F`.
                    fields = dict(command[i + 1].split("=", 1)
                                  for i, value in enumerate(command) if value in ("-f", "-F"))
                    typed = {command[i + 1].split("=", 1)[0]
                             for i, value in enumerate(command) if value == "-F"} - {"query"}
                    self.assertEqual(typed, {"number"} if "number" in fields else set())
                    cursor = fields.get("cursor")
                    if "thread_id" in fields:
                        thread_id = fields["thread_id"]
                        requests.append((thread_id, cursor))
                        expected_cursor = {"thread1": "comment100", "thread2": "other1"}[thread_id]
                        self.assertEqual(cursor, expected_cursor)
                        return json.dumps({"data": {"node": {"comments": connection([
                            {"id": f"{thread_id}-last", "body": "Latest resolution"}
                        ])}}})

                    self.assertEqual((fields["owner"], fields["repo"], fields["number"]),
                                     ("acme", "app", "7"))
                    if "reviewThreads(" in stdin:
                        name = "reviewThreads"
                        if cursor is None:
                            page = connection([{"id": "thread1", "comments": connection(
                                [{"id": str(i), "body": "Earlier comment"} for i in range(100)],
                                "comment100"
                            )}], "threads1")
                        else:
                            self.assertEqual(cursor, "threads1")
                            page = connection([{"id": "thread2", "comments": connection(
                                [{"id": "other-first", "body": "Another concern"}], "other1"
                            )}])
                    elif "reviews(" in stdin:
                        name = "reviews"
                        page = connection([])
                    else:
                        name = "comments"
                        if cursor is None:
                            page = connection([{"id": "conversation1"}], "conversation1")
                        else:
                            self.assertEqual(cursor, "conversation1")
                            page = connection([{"id": "conversation2"}])
                    requests.append((name, cursor))
                    return json.dumps({"data": {"repository": {"pullRequest": {
                        "number": 7, "url": "https://git.acme.test/acme/app/pull/7", "title": "Change",
                        "state": "OPEN", "baseRefName": "main", "headRefName": "feature", name: page,
                    }}}})

                output = io.StringIO()
                with patch.object(module, "run", side_effect=fake_run), patch.object(
                    sys, "argv", ["fetch", "--pr", "https://git.acme.test/acme/app/pull/7#discussion_r1"]
                ), contextlib.redirect_stdout(output):
                    self.assertEqual(module.main(), 0)
                result = json.loads(output.getvalue())
                self.assertEqual(result["pull_request"]["host"], "git.acme.test")
                self.assertEqual(len(result["conversation_comments"]), 2)
                threads = result["review_threads"]
                self.assertEqual([len(thread["comments"]["nodes"]) for thread in threads], [101, 2])
                self.assertEqual(threads[0]["comments"]["nodes"][-1]["body"], "Latest resolution")
                self.assertIn(("reviewThreads", "threads1"), requests)
                self.assertIn(("thread1", "comment100"), requests)
                self.assertIn(("thread2", "other1"), requests)

    def test_missing_comment_page_fails_instead_of_returning_partial_context(self):
        for module in REVIEW_HELPERS:
            with self.subTest(helper=module.__name__):
                thread = {"id": "thread1", "comments": connection([], "next")}
                with patch.object(module, "run", return_value=json.dumps({"data": {"node": None}})):
                    with self.assertRaisesRegex(RuntimeError, "remaining comments"):
                        module.complete_thread_comments("git.acme.test", thread)

    def test_missing_cursor_cannot_silently_end_pagination(self):
        for module in REVIEW_HELPERS:
            with self.subTest(helper=module.__name__):
                thread = {"id": "thread1", "comments": {
                    "nodes": [], "pageInfo": {"hasNextPage": True, "endCursor": None}
                }}
                with self.assertRaisesRegex(RuntimeError, "pagination cursor"):
                    module.complete_thread_comments("git.acme.test", thread)


HEAD = "b5568c0ae64b15d38c336c721404034913c106c6"
OLD_HEAD = "d57114cb82aa31f6c0e0d7f7e5f0c1a2b3c4d5e6"
CODEX = "chatgpt-codex-connector"


def codex_pull_request(reactions=(), reviewed_commits=(), committed="2026-10-01T23:33:05Z",
                       reviewed_at="2026-10-01T23:40:00Z"):
    return {
        "headRefOid": HEAD,
        "commits": {"nodes": [{"commit": {"committedDate": committed}}]},
        "reactions": {"nodes": [
            {"content": content, "createdAt": created, "user": {"login": f"{CODEX}[bot]"}}
            for content, created in reactions
        ]},
        "reviews": {"nodes": [
            {"author": {"login": CODEX}, "submittedAt": reviewed_at, "commit": {"oid": oid}}
            for oid in reviewed_commits
        ]},
    }


def codex_summary(*rows):
    table = "\n".join(
        f"| {name} | {status} <relative-time>2026-10-01</relative-time> | `{commit[:7]}` | New commits |"
        for name, status, commit in rows
    )
    return {"author": {"login": CODEX}, "createdAt": "2026-10-01T09:48:13Z", "body": (
        "<!-- codex-pull-request-review-summary -->\n## Codex Review Summary\n\n"
        "| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n" + table
    )}


class CodexReviewStateTests(OfflineTest):
    def state(self, pull_request, comments=()):
        return WATCHER.codex_review(pull_request, list(comments))["state"]

    def test_eyes_reaction_means_a_review_is_still_running(self):
        summary = codex_summary(("📝 **Code Review**", "✅ **Completed**", HEAD))
        pull_request = codex_pull_request([("EYES", "2026-10-01T23:33:24Z")])
        self.assertEqual(self.state(pull_request, [summary]), "running")

    def test_summary_running_for_head_means_running(self):
        summary = codex_summary(
            ("📝 **Code Review**", "🔄 **Running** since", HEAD),
            ("🔒 **Security Review**", "✅ **Completed**", HEAD),
        )
        self.assertEqual(self.state(codex_pull_request(), [summary]), "running")

    def test_thumbs_up_from_an_earlier_commit_does_not_approve_the_new_head(self):
        summary = codex_summary(("📝 **Code Review**", "✅ **Completed**", OLD_HEAD))
        pull_request = codex_pull_request([("THUMBS_UP", "2026-10-01T12:50:00Z")])
        self.assertEqual(self.state(pull_request, [summary]), "pending")

    def test_completed_head_review_with_findings_is_not_approved(self):
        summary = codex_summary(("📝 **Code Review**", "✅ **Completed**", HEAD))
        pull_request = codex_pull_request([("THUMBS_UP", "2026-10-01T06:00:00Z")], [OLD_HEAD, HEAD])
        self.assertEqual(self.state(pull_request, [summary]), "findings")

    def test_thumbs_up_after_a_head_review_with_findings_means_the_rerun_was_clean(self):
        summary = codex_summary(("📝 **Code Review**", "✅ **Completed**", HEAD))
        pull_request = codex_pull_request([("THUMBS_UP", "2026-10-01T23:50:00Z")], [OLD_HEAD, HEAD])
        self.assertEqual(self.state(pull_request, [summary]), "approved")

    def test_all_head_reviews_completed_with_thumbs_up_is_approved(self):
        summary = codex_summary(
            ("📝 **Code Review**", "✅ **Completed**", HEAD),
            ("🔒 **Security Review**", "✅ **Completed**", HEAD),
        )
        pull_request = codex_pull_request([("THUMBS_UP", "2026-10-01T06:00:00Z")], [OLD_HEAD])
        self.assertEqual(self.state(pull_request, [summary]), "approved")

    def test_unrecognized_head_status_is_reported_as_failed(self):
        summary = codex_summary(("📝 **Code Review**", "❌ **Failed**", HEAD))
        self.assertEqual(self.state(codex_pull_request(), [summary]), "failed")

    def test_without_summary_thumbs_up_must_follow_the_head_commit(self):
        stale = codex_pull_request([("THUMBS_UP", "2026-10-01T23:00:00Z")])
        fresh = codex_pull_request([("THUMBS_UP", "2026-10-01T23:45:00Z")])
        self.assertEqual(self.state(stale), "pending")
        self.assertEqual(self.state(fresh), "approved")

    def test_without_summary_thumbs_up_older_than_codex_last_review_is_not_about_the_head(self):
        # An old-dated commit pushed after an old 👍: the 👍 predates Codex's review of an earlier commit.
        pull_request = codex_pull_request([("THUMBS_UP", "2026-10-01T23:45:00Z")], [OLD_HEAD],
                                          committed="2026-09-30T08:00:00Z", reviewed_at="2026-10-02T08:00:00Z")
        self.assertEqual(self.state(pull_request), "pending")


class ActivityTests(OfflineTest):
    def test_only_other_peoples_items_after_since_count_as_new(self):
        context = {
            "conversation_comments": [
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T10:00:00Z", "url": "old"},
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T12:00:00Z", "url": "new"},
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T10:00:00Z",
                 "updatedAt": "2026-10-01T12:30:00Z", "url": "edited"},
                {"author": {"login": "me"}, "createdAt": "2026-10-01T12:00:00Z", "url": "own-reply"},
                {**codex_summary(("Code Review", "Running", HEAD)), "createdAt": "2026-10-01T12:00:00Z",
                 "url": "summary"},
            ],
            "reviews": [
                {"author": {"login": CODEX}, "state": "COMMENTED", "body": "### 💡 Codex Review",
                 "submittedAt": "2026-10-01T12:05:00Z", "url": "codex-review"},
                {"author": {"login": "reviewer"}, "state": "COMMENTED", "body": "",
                 "submittedAt": "2026-10-01T12:05:00Z", "url": "empty-review-wrapper"},
            ],
            "review_threads": [{"isResolved": False, "comments": {"nodes": [
                {"author": {"login": CODEX}, "createdAt": "2026-10-01T12:05:00Z", "url": "inline"},
                {"author": {"login": "me"}, "createdAt": "2026-10-01T12:10:00Z", "url": "inline-reply"},
            ]}}],
        }
        since = WATCHER.parse_time("2026-10-01T11:00:00Z")
        urls = [item["url"] for item in WATCHER.new_activity(context, "me", since)]
        self.assertEqual(sorted(urls), ["codex-review", "edited", "inline", "new"])


def snapshot(state, activity=(), pr_state="OPEN"):
    return {"pull_request": {"state": pr_state}, "codex": {"state": state},
            "new_activity": list(activity)}


class WatchTests(OfflineTest):
    def watch(self, snapshots, timeout=30):
        sleeps = []

        def sleep(seconds):
            sleeps.append(seconds)

        with patch.object(WATCHER, "check", side_effect=snapshots), \
                patch.object(WATCHER.time, "sleep", side_effect=sleep), \
                patch.object(WATCHER.time, "monotonic", side_effect=lambda: sum(sleeps)):
            result = WATCHER.watch(target=None, since=None, interval=5 * 60, timeout=timeout * 60)
        return result, sleeps

    def test_new_comments_wait_until_codex_finishes(self):
        result, sleeps = self.watch([
            snapshot("running", [{"url": "human"}]),
            snapshot("findings", [{"url": "human"}, {"url": "codex"}]),
        ])
        self.assertEqual(result["reason"], "new-activity")
        self.assertEqual(sleeps, [300])

    def test_codex_approval_wakes_even_without_new_comments(self):
        result, _ = self.watch([snapshot("pending"), snapshot("approved")])
        self.assertEqual(result["reason"], "codex-approved")

    def test_handled_findings_without_new_activity_keep_waiting_until_timeout(self):
        result, sleeps = self.watch([snapshot("findings")] * 10, timeout=12)
        self.assertEqual(result["reason"], "timeout")
        self.assertEqual(result["codex"]["state"], "findings")
        self.assertEqual(sleeps, [300, 300])

    def test_closed_pull_request_stops_the_watch(self):
        result, _ = self.watch([snapshot("running", pr_state="MERGED")])
        self.assertEqual(result["reason"], "closed")


class RelationshipTests(OfflineTest):
    def run_relationship(self, mode, existing_ids, persist_write=True):
        requests = []
        ids = list(existing_ids)
        flag, child_flag, suffix, field = {
            "parent": ("--parent", "--sub-issue", "sub_issues", "sub_issue_id"),
            "blocked": ("--blocked", "--blocked-by", "dependencies/blocked_by", "issue_id"),
        }[mode]

        def fake_run(command):
            requests.append(command)
            self.assertEqual(command[command.index("--hostname") + 1], "git.acme.test")
            if command[1:3] == ["auth", "status"]:
                self.assertIn("--active", command)
                return "Authenticated"
            self.assertEqual(command[1], "api")
            endpoint = next(value for value in command if value.startswith("repos/"))
            if endpoint == "repos/acme/app/issues/7":
                return json.dumps({"id": 2007, "number": 7})
            self.assertEqual(endpoint, f"repos/acme/app/issues/1/{suffix}")
            if "POST" in command:
                self.assertIn(f"{field}=2007", command)
                if persist_write:
                    ids.append(2007)
                return "{}"
            self.assertIn("--paginate", command)
            self.assertIn("--slurp", command)
            # Both repositories have issue #7; only the database ID identifies the target.
            return json.dumps([[{"id": issue_id, "number": 7}] for issue_id in ids])

        output, errors = io.StringIO(), io.StringIO()
        with patch.object(RELATIONSHIPS, "run", side_effect=fake_run), patch.object(
            sys, "argv", ["relationships", "--repo", "git.acme.test/acme/app", flag, "1", child_flag, "7"]
        ), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            status = RELATIONSHIPS.main()
        return status, output.getvalue(), errors.getvalue(), requests

    def test_same_number_in_another_repository_does_not_skip_creation(self):
        for mode in ("parent", "blocked"):
            with self.subTest(mode=mode):
                status, output, errors, requests = self.run_relationship(mode, [9007])
                self.assertEqual(status, 0, errors)
                result = json.loads(output)
                self.assertTrue(result["created"])
                self.assertTrue(result["verified"])
                self.assertEqual(result["repository"], "git.acme.test/acme/app")
                self.assertEqual(sum("POST" in request for request in requests), 1)

    def test_existing_target_on_later_page_is_not_created_again(self):
        for mode in ("parent", "blocked"):
            with self.subTest(mode=mode):
                status, output, errors, requests = self.run_relationship(mode, [9007, 2007])
                self.assertEqual(status, 0, errors)
                self.assertFalse(json.loads(output)["created"])
                self.assertFalse(any("POST" in request for request in requests))

    def test_wrong_issue_in_readback_cannot_verify_a_write(self):
        for mode in ("parent", "blocked"):
            with self.subTest(mode=mode):
                status, output, errors, _ = self.run_relationship(mode, [9007], persist_write=False)
                self.assertEqual(status, 1)
                self.assertEqual(output, "")
                self.assertIn("did not report", errors)

    def test_repository_host_defaults_match_cli_conventions(self):
        with patch.dict("os.environ", {"GH_HOST": "git.acme.test"}):
            self.assertEqual(RELATIONSHIPS.parse_repository("acme/app"), ("git.acme.test", "acme/app"))
            self.assertEqual(RELATIONSHIPS.parse_repository("github.com/acme/app"), ("github.com", "acme/app"))
        with patch.dict("os.environ", {"GH_HOST": ""}):
            self.assertEqual(RELATIONSHIPS.parse_repository("acme/app"), ("github.com", "acme/app"))


if __name__ == "__main__":
    unittest.main()
