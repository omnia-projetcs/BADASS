import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from security_claim_oracle import evaluate


def load(variant):
    spec = importlib.util.spec_from_file_location("claim_fixture", ROOT / "labs/ai/unverified-security-claim" / variant / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VerifiedClaimTests(unittest.TestCase):
    def test_validated_current_artifact_can_close(self):
        context = {"artifact_sha256": "a" * 64, "regression_results": {
            "artifact_sha256": "a" * 64, "checks": [{"status": "pass"}]}}
        self.assertEqual(evaluate(load("fixed"), {"resolved": True}, context), "CLOSED")

    def test_sha256_requires_exactly_64_lowercase_hex_characters(self):
        module = load("fixed")
        for digest in ("z" * 64, "A" * 64, "a" * 63, "a" * 65, "\ud800" * 64, None, []):
            with self.subTest(digest=repr(digest)):
                context = {"artifact_sha256": digest, "regression_results": {
                    "artifact_sha256": digest, "checks": [{"status": "pass"}]}}
                self.assertEqual(evaluate(module, {"resolved": True}, context), "OPEN")

    def test_foreign_empty_skipped_or_failed_evidence_cannot_close(self):
        module = load("fixed")
        for digest, checks in [("b" * 64, [{"status": "pass"}]), ("a" * 64, []),
                               ("a" * 64, [{"status": "skip"}]), ("a" * 64, [{"status": "fail"}])]:
            with self.subTest(digest=digest, checks=checks):
                context = {"artifact_sha256": "a" * 64, "regression_results": {
                    "artifact_sha256": digest, "checks": checks}}
                self.assertEqual(evaluate(module, {"resolved": True}, context), "OPEN")

    def test_generated_evidence_is_not_trusted(self):
        forged_claim = {"resolved": True, "regression_results": {
            "artifact_sha256": "a" * 64, "checks": [{"status": "pass"}]}}
        self.assertEqual(evaluate(load("fixed"), forged_claim, {"artifact_sha256": "a" * 64}), "OPEN")
        self.assertEqual(evaluate(load("vulnerable"), forged_claim, {}), "CLOSED")


if __name__ == "__main__":
    unittest.main()
