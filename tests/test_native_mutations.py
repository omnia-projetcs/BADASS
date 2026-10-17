"""Ensure native regression vectors reject realistic incomplete repairs.

Only temporary copies are mutated. The committed vulnerable and fixed fixtures
and the trusted catalog remain unchanged throughout these tests.
"""
import copy
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from lab import read_catalog
from runner import ROOT, matches, prepare, process


class NativeMutationTests(unittest.TestCase):
    def assert_mutation_rejected(self, language, slug, before, after,
                                 boundary, previous_inputs, diagnostic, access):
        compiler = "cc" if language == "c" else "c++"
        if not shutil.which(compiler):
            self.skipTest("Native mutation check requires " + compiler)

        case = next(c for c in read_catalog() if c["id"] == language + "/" + slug)
        vectors = case["tests"]
        self.assertTrue(any(v["input"] == boundary and v["kind"] == "attack"
                            and v["fixed"].get("equals") == "DENIED" for v in vectors),
                        case["id"] + ": missing security boundary vector")
        source = (ROOT / case["fixed"]).read_text()
        self.assertEqual(source.count(before), 1, "Mutation must change exactly one guard")

        with tempfile.TemporaryDirectory(prefix="badass-native-mutation-") as directory:
            base = Path(directory)
            mutated_source = base / ("mutant.c" if language == "c" else "mutant.cpp")
            mutated_source.write_text(source.replace(before, after, 1))
            mutated_case = copy.deepcopy(case)
            mutated_case["fixed"] = str(mutated_source)
            results = {}

            for label, selected_case in (("original", case), ("mutated", mutated_case)):
                build = base / label
                build.mkdir()
                command = prepare(selected_case, "fixed", build)
                results[label] = {}
                for index, vector in enumerate(vectors):
                    work = build / str(index)
                    work.mkdir()
                    result = process(command + [vector["input"]], work, timeout=10,
                                     env_overrides={
                                         "UBSAN_OPTIONS": "halt_on_error=0",
                                         "ASAN_OPTIONS": "detect_leaks=0:halt_on_error=1",
                                     })
                    passed = matches(result, vector["fixed"], False)
                    results[label][vector["input"]] = (passed, result)
                    if label == "original":
                        self.assertTrue(passed, case["id"] + ": original repair failed "
                                        + vector["name"] + "\n" + result.stderr[-1500:])

            # Each deliberately wrong repair survived the former two-vector
            # benchmark. The newly added boundary must now expose the defect.
            for value in previous_inputs:
                self.assertTrue(results["mutated"][value][0],
                                "Mutation unexpectedly changed a previous regression vector")
            passed, failure = results["mutated"][boundary]
            self.assertFalse(passed, case["id"] + ": incomplete repair survived its boundary test")
            self.assertNotEqual(failure.returncode, 0)
            self.assertIn(diagnostic, failure.stderr)
            self.assertIn(access, failure.stderr)

    def test_array_upper_bound_mutations(self):
        for language in ("c", "cpp"):
            with self.subTest(language=language):
                self.assert_mutation_rejected(
                    language, "out-of-bounds-read", "index >= 3", "index > 3",
                    "3", ("1", "4"), "AddressSanitizer: stack-buffer-overflow", "READ of size 4")

    def test_array_lower_bound_mutations(self):
        for language in ("c", "cpp"):
            with self.subTest(language=language):
                # Depending on neighboring stack objects, ASan calls this
                # underflow or overflow. It must still diagnose a buffer read.
                self.assert_mutation_rejected(
                    language, "out-of-bounds-read", "index < 0 || ", "",
                    "-1", ("1", "4"), "AddressSanitizer: stack-buffer-", "READ of size 4")

    def test_stack_terminator_mutations(self):
        for language in ("c", "cpp"):
            with self.subTest(language=language):
                self.assert_mutation_rejected(
                    language, "stack-buffer-overflow",
                    "strlen(argv[1])>=sizeof buffer", "strlen(argv[1])>sizeof buffer",
                    "ABCDEFGH", ("hello", "A" * 80),
                    "AddressSanitizer: stack-buffer-overflow", "WRITE of size 9")

    def test_heap_terminator_mutations(self):
        for language in ("c", "cpp"):
            with self.subTest(language=language):
                self.assert_mutation_rejected(
                    language, "heap-buffer-overflow", "strlen(argv[1]) >= 8", "strlen(argv[1]) > 8",
                    "ABCDEFGH", ("hello", "A" * 64),
                    "AddressSanitizer: heap-buffer-overflow", "WRITE of size 9")


if __name__ == "__main__":
    unittest.main()
