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
    for name in ("pr-comments-audit", "to-tickets")
]
RELATIONSHIPS = load_helper("relationships", "skills/to-tickets/scripts/set_issue_relationship.py")


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
                    fields = dict(command[i + 1].split("=", 1)
                                  for i, value in enumerate(command) if value == "-F")
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
