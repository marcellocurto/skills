"""Offline behavioral checks for the independently installed GitHub helpers."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
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
ROUND_CODE = load_helper("review_round_code", "skills/babysit-pr/scripts/review_round_code.py")


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


def review(author, body, commit, submitted="2026-10-01T12:00:00Z"):
    return {"author": {"login": author}, "state": "COMMENTED", "body": body,
            "submittedAt": submitted, "commit": {"oid": commit}}


class OwnReviewTests(OfflineTest):
    def summarize(self, reviews):
        return WATCHER.own_reviews(reviews, "me")

    def test_first_review_is_the_viewers_own_lens_review(self):
        summary = self.summarize([
            review("me", "Reviewed `d57114c` for correctness and simplicity: 2 findings, inline.", OLD_HEAD),
            review("reviewer", "Reviewed `b5568c0` by hand", HEAD),
            review("me", "Answered inline.", HEAD),
        ])
        self.assertEqual(summary["first_reviewed_commit"], OLD_HEAD)

    def test_a_new_first_review_after_a_rebase_becomes_the_baseline(self):
        summary = self.summarize([
            review("me", "Reviewed `d57114c` for correctness: 1 finding, inline.", OLD_HEAD),
            review("me", "Reviewed the fixes in `d57114c`: nothing to change.", OLD_HEAD),
            review("me", "Reviewed `b5568c0` for correctness: nothing to change.", HEAD),
        ])
        self.assertEqual(summary["first_reviewed_commit"], HEAD)
        self.assertEqual(summary["last_reviewed_commit"], HEAD)

    def test_without_an_own_lens_review_the_pull_request_has_no_first_review(self):
        summary = self.summarize([
            review("reviewer", "Reviewed `b5568c0` for correctness: looks fine.", HEAD),
            review("me", "Thanks, answered inline.", HEAD),
        ])
        self.assertIsNone(summary["first_reviewed_commit"])
        self.assertIsNone(summary["last_reviewed_commit"])

    def test_last_reviewed_commit_is_the_latest_own_first_review_or_fix_check(self):
        reviewed = [review("me", "Reviewed `d57114c` for correctness: nothing to change.", OLD_HEAD)]
        fix_checked = reviewed + [review("me", "Reviewed the fixes in `b5568c0`: nothing to change.", HEAD)]
        replied = fix_checked + [review("me", "Answered inline.", OLD_HEAD),
                                 review("reviewer", "Reviewed the fixes in `d57114c`.", OLD_HEAD)]
        self.assertEqual(self.summarize(reviewed)["last_reviewed_commit"], OLD_HEAD)
        self.assertEqual(self.summarize(fix_checked)["last_reviewed_commit"], HEAD)
        self.assertEqual(self.summarize(replied)["last_reviewed_commit"], HEAD)

    def test_counts_own_fix_checks(self):
        summary = self.summarize([
            review("me", "Reviewed `d57114c` for correctness: 1 finding, inline.", OLD_HEAD),
            review("me", "Reviewed the fixes in `d57114c`: 1 finding fixed before this push.", OLD_HEAD),
            review("reviewer", "Reviewed the fixes in `b5568c0`: fine by me.", HEAD),
            review("me", "Reviewed the fixes in `b5568c0`: nothing to change.", HEAD),
        ])
        self.assertEqual(summary["fix_checks"], 2)


class ActivityTests(OfflineTest):
    def test_only_other_peoples_items_after_since_count_as_new(self):
        context = {
            "conversation_comments": [
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T10:00:00Z", "url": "old"},
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T12:00:00Z", "url": "new"},
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T10:00:00Z",
                 "updatedAt": "2026-10-01T12:30:00Z", "url": "edited"},
                {"author": {"login": "me"}, "createdAt": "2026-10-01T12:00:00Z", "url": "own-reply"},
            ],
            "reviews": [
                {"author": {"login": "reviewer"}, "state": "CHANGES_REQUESTED", "body": "Please split this.",
                 "submittedAt": "2026-10-01T12:05:00Z", "url": "changes-requested"},
                {"author": {"login": "reviewer"}, "state": "COMMENTED", "body": "",
                 "submittedAt": "2026-10-01T12:05:00Z", "url": "empty-review-wrapper"},
                {"author": {"login": "me"}, "state": "COMMENTED", "body": "Reviewed the fixes in `b5568c0`.",
                 "submittedAt": "2026-10-01T12:06:00Z", "url": "own-review"},
            ],
            "review_threads": [{"isResolved": False, "comments": {"nodes": [
                {"author": {"login": "reviewer"}, "createdAt": "2026-10-01T12:05:00Z", "url": "inline"},
                {"author": {"login": "me"}, "createdAt": "2026-10-01T12:10:00Z", "url": "inline-reply"},
            ]}}],
        }
        since = WATCHER.parse_time("2026-10-01T11:00:00Z")
        urls = [item["url"] for item in WATCHER.new_activity(context, "me", since)]
        self.assertEqual(sorted(urls), ["changes-requested", "edited", "inline", "new"])


def check_run(name, conclusion=None, completed_at=None, required=False):
    return {"__typename": "CheckRun", "name": name, "status": "COMPLETED" if conclusion else "IN_PROGRESS",
            "conclusion": conclusion, "completedAt": completed_at, "detailsUrl": f"https://ci/{name}",
            "isRequired": required}


def status_context(name, state, created_at="2026-10-01T12:00:00Z", required=False):
    return {"__typename": "StatusContext", "context": name, "state": state, "createdAt": created_at,
            "targetUrl": f"https://ci/{name}", "isRequired": required}


class CheckSummaryTests(OfflineTest):
    def test_lists_failing_and_unfinished_checks_with_whether_they_are_required(self):
        summary = WATCHER.summarize_checks([
            check_run("lint", "SUCCESS", "2026-10-01T12:00:00Z", required=True),
            check_run("test", "FAILURE", "2026-10-01T12:05:00Z", required=True),
            check_run("e2e", "TIMED_OUT", "2026-10-01T12:06:00Z"),
            check_run("docs", "SKIPPED", "2026-10-01T12:01:00Z"),
            check_run("build", required=True),
            status_context("deploy-preview", "PENDING"),
            status_context("license", "ERROR", "2026-10-01T12:07:00Z"),
        ])
        self.assertEqual([(c["name"], c["required"]) for c in summary["failing"]],
                         [("test", True), ("e2e", False), ("license", False)])
        self.assertEqual([(c["name"], c["required"]) for c in summary["pending"]],
                         [("build", True), ("deploy-preview", False)])
        self.assertEqual(summary["last_completed_at"], "2026-10-01T12:07:00Z")

    def test_a_commit_without_checks_has_nothing_failing_or_pending(self):
        summary = WATCHER.summarize_checks([])
        self.assertEqual((summary["failing"], summary["pending"], summary["last_completed_at"]), ([], [], None))


def snapshot(activity=(), pr_state="OPEN", failing=(), pending=(), last_completed_at=None, mergeable="MERGEABLE"):
    return {"pull_request": {"state": pr_state, "mergeable": mergeable}, "new_activity": list(activity),
            "checks": {"failing": list(failing), "pending": list(pending), "last_completed_at": last_completed_at}}


SINCE = "2026-10-01T11:00:00Z"
BEFORE_SINCE = "2026-10-01T10:00:00Z"
AFTER_SINCE = "2026-10-01T12:00:00Z"


class WatchTests(OfflineTest):
    def watch(self, snapshots, timeout=30, since=None):
        sleeps = []

        def sleep(seconds):
            sleeps.append(seconds)

        with patch.object(WATCHER, "check", side_effect=snapshots), \
                patch.object(WATCHER.time, "sleep", side_effect=sleep), \
                patch.object(WATCHER.time, "monotonic", side_effect=lambda: sum(sleeps)):
            result = WATCHER.watch(target=None, since=since and WATCHER.parse_time(since),
                                   interval=5 * 60, timeout=timeout * 60)
        return result, sleeps

    def test_a_new_comment_wakes_the_watch(self):
        result, sleeps = self.watch([snapshot(), snapshot([{"url": "human"}])])
        self.assertEqual(result["reason"], "new-activity")
        self.assertEqual(sleeps, [300])

    def test_without_new_activity_the_watch_waits_until_timeout(self):
        result, sleeps = self.watch([snapshot()] * 10, timeout=12)
        self.assertEqual(result["reason"], "timeout")
        self.assertEqual(sleeps, [300, 300])

    def test_closed_pull_request_stops_the_watch(self):
        result, _ = self.watch([snapshot([{"url": "human"}], pr_state="MERGED")])
        self.assertEqual(result["reason"], "closed")

    def test_a_check_failing_after_since_wakes_the_watch(self):
        failed = {"name": "test", "completed_at": AFTER_SINCE}
        result, sleeps = self.watch([snapshot(pending=[{"name": "test"}]),
                                     snapshot(failing=[failed], pending=[{"name": "e2e"}])], since=SINCE)
        self.assertEqual(result["reason"], "check-failed")
        self.assertEqual(sleeps, [300])

    def test_a_failure_already_seen_before_since_does_not_wake_the_watch(self):
        failed = {"name": "test", "completed_at": BEFORE_SINCE}
        result, _ = self.watch([snapshot(failing=[failed], last_completed_at=BEFORE_SINCE)] * 10,
                               timeout=12, since=SINCE)
        self.assertEqual(result["reason"], "timeout")

    def test_the_last_pending_check_finishing_wakes_the_watch(self):
        result, sleeps = self.watch([snapshot(pending=[{"name": "build"}], last_completed_at=BEFORE_SINCE),
                                     snapshot(last_completed_at=AFTER_SINCE)], since=SINCE)
        self.assertEqual(result["reason"], "checks-finished")
        self.assertEqual(sleeps, [300])

    def test_a_merge_conflict_wakes_the_watch(self):
        result, sleeps = self.watch([snapshot(mergeable="UNKNOWN"), snapshot(mergeable="CONFLICTING")],
                                    since=SINCE)
        self.assertEqual(result["reason"], "conflict")
        self.assertEqual(sleeps, [300])


# Long enough lines for `git blame -C` to recognise a moved block.
ORIGINAL_BLOCK = "".join(f"def original_rule_{n}(value):\n    return value * {n} + {n}\n" for n in range(1, 5))


class ReviewRoundCodeTests(unittest.TestCase):
    """Runs real git, since move detection by `git blame` is part of what is checked."""

    def setUp(self):
        self.repo = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                    "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
        self.git("init", "-q", "-b", "main")
        self.commit({"app.py": "print('base')\n"}, "base")
        self.git("checkout", "-q", "-b", "feature")
        self.first_reviewed = self.commit({"app.py": "print('base')\n" + ORIGINAL_BLOCK}, "PR as opened")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env, check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self, files, message):
        for name, content in files.items():
            (self.repo / name).write_text(content)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def flag(self, path, start, end):
        thread = {"path": path, "startLine": start, "line": end, "diffSide": "RIGHT",
                  "comments": {"nodes": [{"url": "https://github.com/acme/app/pull/7#r1"}]}}
        return ROUND_CODE.flag_thread(thread, self.first_reviewed, "main", self.repo)

    def test_lines_added_after_the_first_review_are_flagged_with_their_commit(self):
        fix = self.commit({"app.py": "print('base')\n" + ORIGINAL_BLOCK + "GUARD = True\n"}, "review fix")
        self.assertEqual(self.flag("app.py", 10, 10)["added_after_first_review"], True)
        self.assertEqual(self.flag("app.py", 10, 10)["commits"], [fix])
        self.assertEqual(self.flag("app.py", 2, 9)["added_after_first_review"], False)

    def test_code_moved_to_another_file_after_the_first_review_keeps_its_origin(self):
        self.commit({"app.py": "print('base')\n", "rules.py": ORIGINAL_BLOCK}, "move rules")
        self.assertEqual(self.flag("rules.py", 1, 8)["added_after_first_review"], False)

    def test_code_merged_in_from_the_base_branch_is_not_review_round_code(self):
        self.git("checkout", "-q", "main")
        self.commit({"other.py": "print('from main')\n"}, "main moves on")
        self.git("checkout", "-q", "feature")
        self.git("merge", "-q", "--no-edit", "main")
        self.assertEqual(self.flag("other.py", 1, 1)["added_after_first_review"], False)

    def test_threads_without_a_current_line_cannot_be_judged(self):
        thread = {"path": "app.py", "startLine": None, "line": None, "diffSide": "RIGHT",
                  "comments": {"nodes": [{"url": "u"}]}}
        self.assertIsNone(ROUND_CODE.flag_thread(thread, self.first_reviewed, "main", self.repo)
                          ["added_after_first_review"])


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
