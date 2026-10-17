import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from export_blind import export, normalize
from lab import read_catalog, score


class BlindExportTests(unittest.TestCase):
    def test_ground_truth_stays_outside_corpus_and_round_trips(self):
        case = next(c for c in read_catalog() if c["id"] == "python/sql-injection")
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus"
            key = Path(directory) / "private/mapping.json"
            result = export([case], corpus, key)
            self.assertEqual(result["sources"], 2)
            paths = list(corpus.rglob("*"))
            self.assertFalse(any(p.suffix == ".json" or p.name == "README.md" for p in paths))
            self.assertFalse(any("vulnerable" in str(p.relative_to(corpus)) or "fixed" in str(p.relative_to(corpus)) for p in paths))
            manifest = json.loads(key.read_text())
            path = next(p for p, data in manifest["files"].items() if data["variant"] == "vulnerable")
            findings = normalize([{"path": path, "cwe": "CWE-89"}], manifest)
            self.assertEqual(score([case], findings)["true_positives"], 1)
            with self.assertRaises(ValueError):
                normalize([{"path": "../private/mapping.json", "cwe": "CWE-89"}], manifest)

    def test_mapping_inside_corpus_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "corpus"
            with self.assertRaises(ValueError):
                export(read_catalog()[:1], output, output / "answers.json")

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                export(read_catalog()[:1], Path(directory), Path(directory).parent / "never-written.json")


if __name__ == "__main__":
    unittest.main()
