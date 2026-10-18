"""Observe child-process options, format traversal and atomic file creation."""
from pathlib import Path
import tempfile
import threading
import unittest

from test_exploitdb_cases import load


class ArgumentBoundaryTests(unittest.TestCase):
    def test_actual_child_tool_exposes_private_records_only_before_repair(self):
        for variant in ("vulnerable", "fixed"):
            module = load("argument-injection", variant)
            with self.subTest(variant=variant):
                result = module.run("--include-private")
                self.assertEqual(result["status"], 200)
                self.assertEqual("LAB_PRIVATE_REPORT" in result["matches"], variant == "vulnerable")
                self.assertEqual(module.run("report"), {"status": 200, "matches": ["PUBLIC_REPORT"]})

    def test_fixed_preserves_option_like_and_shell_like_queries_as_data(self):
        module = load("argument-injection", "fixed")
        for value in ("--include-private", "--help", "-h", "--unknown", "x; echo marker", "$(echo marker)"):
            with self.subTest(value=value):
                self.assertEqual(module.run(value), {"status": 200, "matches": []})


class FormatBoundaryTests(unittest.TestCase):
    def test_disclosure_reads_real_object_data_and_fixed_rejects_traversal(self):
        for variant in ("vulnerable", "fixed"):
            module = load("format-string-disclosure", variant)
            profile = module.Profile()
            profile.private["api_key"] = "UNIQUE_SYNTHETIC_KEY"
            with self.subTest(variant=variant):
                template = "{profile.__dict__[private][api_key]}"
                if variant == "vulnerable":
                    self.assertEqual(module.render(template, profile), "UNIQUE_SYNTHETIC_KEY")
                else:
                    with self.assertRaises(ValueError):
                        module.render(template, profile)

    def test_fixed_renders_custom_public_data_without_recursive_evaluation(self):
        module = load("format-string-disclosure", "fixed")
        profile = module.Profile()
        profile.name = "{profile.private[api_key]}"
        profile.team = "Research & QA"
        self.assertEqual(module.render("{{greeting}} {name} / {team}", profile),
                         "{greeting} {profile.private[api_key]} / Research & QA")
        for template in ("{name.__class__}", "{name[0]}", "{name:{profile.private[api_key]}}", "{name!r}"):
            with self.subTest(template=template), self.assertRaises(ValueError):
                module.render(template, profile)


class AtomicCreationTests(unittest.TestCase):
    def test_symlink_inserted_after_check_cannot_redirect_fixed_write(self):
        for variant in ("vulnerable", "fixed"):
            module = load("file-create-race", variant)
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target, victim = root / "report.txt", root / "private.txt"
                victim.write_text("UNIQUE_ORIGINAL")
                checkpoints = []

                def replace_after_check():
                    self.assertFalse(target.exists())
                    checkpoints.append(True)
                    target.symlink_to(victim)

                result = module.write_report(target, "REPLACEMENT", replace_after_check)
                self.assertEqual(checkpoints, [True])
                self.assertEqual(result, {"status": 201 if variant == "vulnerable" else 409})
                self.assertTrue(target.is_symlink())
                self.assertEqual(victim.read_text(), "REPLACEMENT" if variant == "vulnerable" else "UNIQUE_ORIGINAL")

    def test_two_real_writers_both_check_before_either_opens(self):
        for variant in ("vulnerable", "fixed"):
            module = load("file-create-race", variant)
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "report.txt"
                barrier = threading.Barrier(2, timeout=3)
                results, failures = {}, []

                def writer(text):
                    try:
                        results[text] = module.write_report(target, text, barrier.wait)
                    except BaseException as error:
                        failures.append(error)

                threads = [threading.Thread(target=writer, args=(value,), daemon=True) for value in ("FIRST", "OTHER")]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(5)
                self.assertFalse(any(thread.is_alive() for thread in threads))
                self.assertEqual(failures, [])
                statuses = sorted(result["status"] for result in results.values())
                self.assertEqual(statuses, [201, 201] if variant == "vulnerable" else [201, 409])
                accepted = [text for text, result in results.items() if result["status"] == 201]
                self.assertIn(target.read_text(), accepted)

    def test_preexisting_regular_file_and_symlink_are_not_overwritten(self):
        for variant in ("vulnerable", "fixed"):
            module = load("file-create-race", variant)
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                existing = root / "existing.txt"
                existing.write_text("KEEP")
                link = root / "link.txt"
                link.symlink_to(existing)
                for path in (existing, link):
                    self.assertEqual(module.write_report(path, "REPLACE"), {"status": 409})
                    self.assertEqual(existing.read_text(), "KEEP")


if __name__ == "__main__":
    unittest.main()
