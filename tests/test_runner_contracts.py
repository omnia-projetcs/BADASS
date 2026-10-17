import copy
import json
from pathlib import Path
from subprocess import CompletedProcess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from lab import read_catalog, validate
from runner import file_matches, matches, process, run_cases


class RunnerContractTests(unittest.TestCase):
    def test_empty_run_is_a_failure(self):
        self.assertEqual(run_cases([]), ([], True))

    def test_all_skipped_run_is_a_failure_even_without_strict(self):
        case = next(c for c in read_catalog() if c["language"] == "go")
        with patch("runner.shutil.which", return_value=None):
            records, failed = run_cases([case])
        self.assertTrue(failed)
        self.assertEqual(records[0]["status"], "skip")

    def test_spaces_and_tabs_are_observable(self):
        self.assertTrue(matches(CompletedProcess([], 0, " hello \n", ""), {"equals": " hello "}, False))
        self.assertFalse(matches(CompletedProcess([], 0, "hello\n", ""), {"equals": " hello "}, False))
        self.assertFalse(matches(CompletedProcess([], 0, "hello\t", ""), {"equals": "hello"}, False))

    def test_explicit_exit_contract_is_required(self):
        result = CompletedProcess([], 2, "", "")
        self.assertFalse(matches(result, {"equals": ""}, False))
        self.assertTrue(matches(result, {"equals": "", "exit_code": 2}, False))

    def test_file_assertions_detect_noop_and_wrong_permissions(self):
        expected = [{"path": "export.txt", "type": "file", "content": "SECRET", "mode": "0600"}]
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(file_matches(directory, expected))
            path = Path(directory) / "export.txt"
            path.write_text("SECRET")
            path.chmod(0o600)
            self.assertTrue(file_matches(directory, expected))
            path.chmod(0o644)
            self.assertFalse(file_matches(directory, expected))

    def test_observer_refuses_links_and_parent_paths_outside_workdir(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            (Path(outside) / "secret").write_text("SECRET")
            (Path(directory) / "external").symlink_to(outside, target_is_directory=True)
            self.assertFalse(file_matches(directory, [{"path": "external/secret", "content": "SECRET"}]))
            self.assertFalse(file_matches(directory, [{"path": "../secret", "content": "SECRET"}]))

    def test_uncheckable_observation_fields_are_rejected_by_catalog_and_observer(self):
        observations = [
            {"path": "ghost", "type": "absent", "content": "must exist"},
            {"path": "ghost", "type": "absent", "mode": "0600"},
            {"path": "link", "type": "symlink", "target": "target", "content": "WRONG CONTENT"},
            {"path": "link", "type": "symlink", "target": "target", "mode": "0777"},
            {"path": "target", "type": "file", "target": "elsewhere"},
        ]
        baseline = read_catalog()[0]
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "target").write_text("ACTUAL CONTENT")
            (Path(directory) / "link").symlink_to("target")
            for observation in observations:
                with self.subTest(observation=observation):
                    case = copy.deepcopy(baseline)
                    for variant in ("vulnerable", "fixed"):
                        case["tests"][0][variant]["files"] = [observation]
                    with self.assertRaises(AssertionError):
                        validate([case])
                    self.assertFalse(file_matches(directory, [observation]))

    def test_malformed_observations_fail_safely_without_catalog_validation(self):
        invalid = [
            None, {}, "files", 7, [None], [{}],
            [{"path": None}], [{"path": 7}], [{"path": ""}], [{"path": "."}],
            [{"path": "bad\x00name"}], [{"path": "file", "type": []}],
            [{"path": "file", "content": None}], [{"path": "file", "content": "\ud800"}],
            [{"path": "file", "mode": 0o600}], [{"path": "file", "mode": "0999"}],
            [{"path": "link", "type": "symlink"}],
            [{"path": "link", "type": "symlink", "target": 7}],
            [{"path": "link", "type": "symlink", "target": ""}],
            [{"path": "link", "type": "symlink", "target": "bad\x00target"}],
        ]
        baseline = read_catalog()[0]
        with tempfile.TemporaryDirectory() as directory:
            for observations in invalid:
                with self.subTest(observations=observations):
                    self.assertFalse(file_matches(directory, observations))
                    case = copy.deepcopy(baseline)
                    for variant in ("vulnerable", "fixed"):
                        case["tests"][0][variant]["files"] = observations
                    with self.assertRaises(AssertionError):
                        validate([case])

    def test_valid_absent_file_and_dangling_link_observations_still_work(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file"
            path.write_text("CONTENT")
            path.chmod(0o600)
            (Path(directory) / "link").symlink_to("missing-target")
            self.assertTrue(file_matches(directory, [
                {"path": "ghost", "type": "absent"},
                {"path": "file", "content": "CONTENT", "mode": "0600"},
                {"path": "link", "type": "symlink", "target": "missing-target"},
            ]))
            self.assertFalse(file_matches(directory, [{"path": "link", "type": "absent"}]))

    def test_invalid_workdir_or_parent_link_loop_fails_safely(self):
        self.assertFalse(file_matches(None, []))
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            self.assertFalse(file_matches(base / "missing", []))
            (base / "loop").symlink_to("loop", target_is_directory=True)
            self.assertFalse(file_matches(base, [{"path": "loop/child", "type": "file"}]))

    def test_host_password_does_not_leak_into_fixtures(self):
        command = [sys.executable, "-c", "import os;print(os.environ.get('BADASS_ADMIN_PASSWORD','ABSENT'))"]
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"BADASS_ADMIN_PASSWORD": "HOST_SECRET"}):
            self.assertEqual(process(command, directory).stdout.strip(), "ABSENT")
            result = process(command, directory, env_overrides={"BADASS_ADMIN_PASSWORD": "LAB_CONFIGURED"})
            self.assertEqual(result.stdout.strip(), "LAB_CONFIGURED")

    def test_catalog_rejects_runtime_control_environment(self):
        case = copy.deepcopy(read_catalog()[0])
        case["tests"][0]["env"] = {"LD_PRELOAD": "/tmp/anything"}
        with self.assertRaises(AssertionError):
            validate([case])


if __name__ == "__main__":
    unittest.main()
