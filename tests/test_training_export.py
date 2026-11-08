"""Check current training data, source fidelity, labels and companion packaging."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from export_training import DEFAULT_OUTPUT, DETECT, REPAIR, SYSTEM, canonical, main, render, source_files
from lab import read_catalog


class TrainingExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = read_catalog()
        cls.content = DEFAULT_OUTPUT.read_text(encoding="utf-8")
        cls.records = [json.loads(line) for line in cls.content.splitlines()]

    def test_committed_file_is_current_deterministic_and_deduplicated(self):
        self.assertEqual(self.content, render(self.cases))
        self.assertEqual(render(list(reversed(self.cases))), self.content)
        self.assertEqual(len({canonical(record) for record in self.records}), len(self.records))
        self.assertTrue(self.content.endswith("\n"))

    def test_message_schema_and_nested_json_labels(self):
        for record in self.records:
            self.assertEqual(set(record), {"messages"})
            messages = record["messages"]
            self.assertEqual([m["role"] for m in messages], ["system", "user", "assistant"])
            for message in messages:
                self.assertEqual(set(message), {"role", "content"})
                self.assertIsInstance(message["content"], str)
            self.assertEqual(messages[0]["content"], SYSTEM)
            request, answer = [json.loads(m["content"]) for m in messages[1:]]
            self.assertEqual(set(request), {"files", "instruction", "scope", "target_cwe"})
            self.assertTrue(request["files"])
            for name, text in request["files"].items():
                self.assertFalse(Path(name).is_absolute())
                self.assertNotIn("..", Path(name).parts)
                self.assertIsInstance(text, str)
            if request["instruction"] == DETECT:
                self.assertEqual(set(answer), {"cwe", "explanation", "scope", "target_vulnerable"})
                self.assertIs(type(answer["target_vulnerable"]), bool)
                self.assertEqual(answer["cwe"], request["target_cwe"] if answer["target_vulnerable"] else [])
            else:
                self.assertEqual(request["instruction"], REPAIR)
                self.assertEqual(set(answer), {"cwe", "explanation", "files"})
                self.assertEqual(answer["cwe"], request["target_cwe"])

    def test_every_case_has_positive_negative_and_current_repair_sources(self):
        observed = set()
        for record in self.records:
            request, answer = [json.loads(m["content"]) for m in record["messages"][1:]]
            task = "repair" if request["instruction"] == REPAIR else answer["target_vulnerable"]
            for name, text in request["files"].items():
                observed.add((request["scope"], tuple(request["target_cwe"]), task, name, text,
                              answer.get("files", {}).get(name) if task == "repair" else None))
        for case in self.cases:
            vulnerable = ROOT / case["vulnerable"]
            fixed = ROOT / case["fixed"]
            prefix = (case["scope"], tuple(case["cwe"]))
            with self.subTest(case=case["id"]):
                self.assertIn((*prefix, True, vulnerable.name, vulnerable.read_text(), None), observed)
                self.assertIn((*prefix, False, fixed.name, fixed.read_text(), None), observed)
                self.assertIn((*prefix, "repair", vulnerable.name, vulnerable.read_text(), fixed.read_text()), observed)

    def test_recursive_dependency_and_dotnet_companions_are_preserved(self):
        for cid, required in [
            ("node/vulnerable-transitive-dependency", {"main.js", ".npmrc", "package.json", "package-lock.json",
                                                      "settings-wrapper/index.js", "settings-wrapper/package.json"}),
            ("dotnet/xss", {"Program.cs", "Lab.csproj"}),
        ]:
            case = next(c for c in self.cases if c["id"] == cid)
            for variant in ("vulnerable", "fixed"):
                files = source_files(case, variant)
                self.assertEqual(set(files), required)
                base = (ROOT / case[variant]).parent
                for name, text in files.items():
                    self.assertEqual(text, (base / name).read_text())

    def test_generated_artifacts_and_local_configuration_are_not_packaged(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "main.py").write_text("def run(value): return value\n")
            (base / "README.md").write_text("Vulnerability answer key")
            (base / ".env").write_text("LOCAL_CONFIG=private")
            for folder in ("node_modules", "__pycache__", "obj"):
                (base / folder).mkdir()
                (base / folder / "generated.py").write_text("IGNORE")
            (base / "external.py").symlink_to(base / "main.py")
            case = {"vulnerable": str(base / "main.py")}
            self.assertEqual(source_files(case, "vulnerable"), {"main.py": "def run(value): return value\n"})

    def test_check_mode_detects_staleness_and_never_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "training.jsonl"
            self.assertEqual(main(["--check", "--output", str(output)]), 1)
            self.assertFalse(output.exists())
            self.assertEqual(main(["--output", str(output)]), 0)
            self.assertEqual(main(["--check", "--output", str(output)]), 0)
            output.write_text("{}\n")
            self.assertEqual(main(["--check", "--output", str(output)]), 1)
            self.assertEqual(output.read_text(), "{}\n")


if __name__ == "__main__":
    unittest.main()
