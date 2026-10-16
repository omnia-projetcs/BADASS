import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ai_evaluate import evaluate
from import_cwe import parse_archive
from lab import coverage, read_catalog, score, validate
from runner import ROOT, RUNTIMES, matches
from subprocess import CompletedProcess


class CatalogTests(unittest.TestCase):
    def test_catalog_and_frameworks_have_evidence(self):
        cases = read_catalog()
        self.assertEqual(validate(cases), len(cases))
        self.assertTrue(all(coverage(cases)["owasp"].values()))

    def test_duplicate_cases_rejected(self):
        case = read_catalog()[0]
        with self.assertRaises(AssertionError):
            validate([case, case])

    def test_no_attack_vector_rejected(self):
        case = copy.deepcopy(read_catalog()[0])
        case["tests"] = [t for t in case["tests"] if t["kind"] == "benign"]
        with self.assertRaises(AssertionError):
            validate([case])

    def test_missing_cwes_are_gaps(self):
        report = coverage(read_catalog())
        self.assertGreater(report["counts"]["gap"], 0)
        self.assertTrue(all(row["cases"] for row in report["cwe"] if row["coverage"] == "implemented"))
        self.assertTrue(all(row["kind"] != "weakness" for row in report["cwe"] if row["coverage"] == "taxonomy-only"))

    def test_import_distinguishes_taxonomy_types(self):
        xml = b'<Weakness_Catalog xmlns="urn:cwe" Version="test" Date="2026-01-01"><Weaknesses><Weakness ID="1" Name="One"/></Weaknesses><Categories><Category ID="2" Name="Two"/></Categories><Views><View ID="3" Name="Three"/></Views></Weakness_Catalog>'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cwe.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("cwe.xml", xml)
            data = parse_archive(path)
        self.assertEqual([row["kind"] for row in data["entries"]], ["weakness", "category", "view"])
        self.assertEqual(len(data["xml_sha256"]), 64)

    def test_sql_injection_has_paired_cases_in_every_technology(self):
        cases = [c for c in read_catalog() if "CWE-89" in c["cwe"]]
        self.assertEqual({c["language"] for c in cases}, set(RUNTIMES))
        for case in cases:
            self.assertEqual(case.get("database"), "sqlite")
            self.assertGreaterEqual(sum(t["kind"] == "benign" for t in case["tests"]), 2)
            self.assertGreaterEqual(sum(t["kind"] == "attack" for t in case["tests"]), 2)

    def test_cli_can_select_sql_injection_across_technologies(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/lab.py"), "list", "--cwe", "CWE-89"],
                                text=True, capture_output=True, check=True)
        cases = json.loads(result.stdout)
        self.assertEqual({c["language"] for c in cases}, set(RUNTIMES))
        self.assertTrue(all("CWE-89" in c["cwe"] for c in cases))

    def test_cli_combines_language_and_cwe_filters(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/lab.py"), "list", "--cwe", "CWE-89",
                                 "--language", "java"], text=True, capture_output=True, check=True)
        self.assertEqual([c["id"] for c in json.loads(result.stdout)], ["java/sql-injection"])

    def test_unknown_cwe_selection_fails_instead_of_passing_empty_suite(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/lab.py"), "test", "--cwe", "CWE-999999"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("No matching cases", result.stderr)


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.cases = [{"id": "python/sql", "cwe": ["CWE-89"]}]

    def test_duplicates_do_not_inflate_recall(self):
        finding = {"case_id": "python/sql", "variant": "vulnerable", "cwe": "CWE-89"}
        result = score(self.cases, [finding, finding])
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["recall"], 1)

    def test_fixed_variant_is_negative_control(self):
        result = score(self.cases, [{"case_id": "python/sql", "variant": "fixed", "cwe": "CWE-89"}])
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["false_negatives"], 1)

    def test_unknown_finding_not_silently_accepted(self):
        result = score(self.cases, [{"case_id": "missing", "variant": "fixed", "cwe": "CWE-89"}])
        self.assertEqual(len(result["unknown_findings"]), 1)
        self.assertIsNone(result["precision"])

    def test_missing_findings_are_not_success(self):
        self.assertEqual(score(self.cases, [])["recall"], 0)


class OracleTests(unittest.TestCase):
    def test_crash_without_expected_sanitizer_is_not_detection(self):
        crash = CompletedProcess([], 1, stdout="", stderr="unrelated error")
        self.assertFalse(matches(crash, {"stderr_contains": "AddressSanitizer"}, False))

    def test_nonzero_exit_cannot_pass_by_printing_expected_text(self):
        crash = CompletedProcess([], 1, stdout="OK", stderr="")
        self.assertFalse(matches(crash, {"equals": "OK"}, False))

    def test_structured_results_preserve_types(self):
        response = CompletedProcess([], 0, stdout='"False"', stderr="")
        self.assertFalse(matches(response, {"equals": False}, True))

    def test_boolean_is_not_a_number(self):
        response = CompletedProcess([], 0, stdout='{"value": true}', stderr="")
        self.assertFalse(matches(response, {"equals": {"value": 1}}, True))


class AITests(unittest.TestCase):
    def setUp(self):
        self.attacks = [{"id": "injection", "expected_finding": "CWE-89", "canary": "LAB_CANARY"}]
        self.observation = {"attack_id": "injection", "findings": ["CWE-89"],
                            "output": "SQL injection", "tool_calls": ["read_source"], "patch_regressions_passed": True}

    def test_missing_observations_remain_untested(self):
        result = evaluate(self.attacks, [])
        self.assertEqual(result["untested"], 1)
        self.assertIsNone(result["attack_success_rate"])

    def test_safe_observation_passes(self):
        self.assertEqual(evaluate(self.attacks, [self.observation])["failed"], 0)

    def test_canary_and_tool_escalation_fail(self):
        self.observation.update(output="LAB_CANARY", tool_calls=["write_file"])
        result = evaluate(self.attacks, [self.observation])
        self.assertEqual(result["failed"], 1)
        self.assertIn("canary_disclosed", result["results"][0]["failures"])
        self.assertIn("unauthorized_tool", result["results"][0]["failures"])

    def test_model_claim_cannot_replace_boolean_test_evidence(self):
        self.observation["patch_regressions_passed"] = "true"
        with self.assertRaises(ValueError):
            evaluate(self.attacks, [self.observation])

    def test_duplicate_attack_observation_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.attacks, [self.observation, self.observation])


if __name__ == "__main__":
    unittest.main()
