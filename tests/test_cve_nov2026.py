"""Verify the November 2026 named CVE models (phpAfterShell, PHP-FPM, Java4Shell, NGINX2Root)."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from test_named_cves import load, workspace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lab import read_catalog, validate
from runner import prepare, process, run_cases

NOV2026_IDS = {
    "python/phpaftershell-session-overwrite": "CVE-2026-126714",
    "python/php-session-serializer-mismatch": "CVE-2026-115560",
    "python/php-fpm-request-smuggling": "CVE-2026-129289",
    "c/java4shell-base64-overflow": "CVE-2026-114938",
    "c/nginx-http2-flow-overflow": "CVE-2026-123007",
}


class Nov2026CatalogTests(unittest.TestCase):
    def test_nov2026_contracts_validate_and_run(self):
        catalog = read_catalog()
        self.assertEqual(validate(catalog), len(catalog))
        cases = [c for c in catalog if c["id"] in NOV2026_IDS]
        self.assertEqual({c["id"] for c in cases}, set(NOV2026_IDS))
        for case in cases:
            self.assertEqual(case["cve"], [NOV2026_IDS[case["id"]]])
            self.assertTrue(case["references"])
            for kind in ("benign", "attack", "robustness"):
                self.assertTrue(any(t["kind"] == kind for t in case["tests"]), (case["id"], kind))
        if not shutil.which("cc"):
            cases = [c for c in cases if c["language"] != "c"]
        records, failed = run_cases(cases, strict=True)
        self.assertFalse(failed, json.dumps(records, indent=2))
        self.assertEqual(sum(len(r["checks"]) for r in records), 2 * sum(len(c["tests"]) for c in cases))


@unittest.skipUnless(shutil.which("cc"), "Native CVE regressions require a C compiler")
class Nov2026NativeEvidenceTests(unittest.TestCase):
    def test_asan_observes_heap_buffer_overflow_in_java4shell_and_nginx2root(self):
        probes = [
            ("c/java4shell-base64-overflow", "QUJDREVGR0hJSktMTU5PUA==", "heap-buffer-overflow", "WRITE of size"),
            ("c/nginx-http2-flow-overflow", "4294967288:AAAAAAAAAAAAAAAAAAAA", "heap-buffer-overflow", "WRITE of size"),
        ]
        catalog = read_catalog()
        for cid, value, diagnostic, access in probes:
            case = next(c for c in catalog if c["id"] == cid)
            with self.subTest(case=cid), tempfile.TemporaryDirectory() as directory:
                build = Path(directory)
                command = prepare(case, "vulnerable", build)
                result = process(
                    command + [value],
                    build,
                    env_overrides={"ASAN_OPTIONS": "detect_leaks=0:halt_on_error=1"},
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("AddressSanitizer: " + diagnostic, result.stderr)
                self.assertIn(access, result.stderr)
                self.assertIn(case["vulnerable"], result.stderr)


class Nov2026HandlerEvidenceTests(unittest.TestCase):
    def test_phpaftershell_interrupted_overwrite_triggers_gadget_only_when_vulnerable(self):
        payload = {
            "initial": 'note|s:3:"old";g|O:6:"Runner":1:{s:3:"cmd";s:2:"id";}',
            "update": 'note|s:3:"new";tail|s:4:"done";',
            "interrupt_at": 15,
        }
        for variant in ("vulnerable", "fixed"):
            module = load("phpaftershell-session-overwrite", variant)
            with self.subTest(variant=variant), workspace() as work:
                result = module.run(payload)
                marker = work / "gadget-ran.txt"
                self.assertEqual(marker.exists(), variant == "vulnerable")
                if variant == "vulnerable":
                    self.assertEqual(result["objects"], ["Runner"])
                else:
                    self.assertEqual(result["status"], 409)

    def test_php_serializer_mismatch_injects_object_only_when_vulnerable(self):
        payload = {"upload_key": 'x|O:6:"Runner":1:{s:3:"tag";s:5:"pwned";}', "note": "ok"}
        for variant in ("vulnerable", "fixed"):
            module = load("php-session-serializer-mismatch", variant)
            with self.subTest(variant=variant), workspace() as work:
                result = module.run(payload)
                marker = work / "deserialized-object.txt"
                self.assertEqual(marker.exists(), variant == "vulnerable")
                if variant == "vulnerable":
                    self.assertEqual(result["objects"], ["Runner"])
                else:
                    self.assertEqual(result["status"], 400)

    def test_php_fpm_smuggling_executes_smuggled_script_only_when_vulnerable(self):
        payload = {
            "wire": "SCRIPT=/var/www/public.php\nLENGTH=40\n\nabcdSCRIPT=/var/www/admin.php\nLENGTH=0\n\n",
            "read_limit": 4,
        }
        for variant in ("vulnerable", "fixed"):
            module = load("php-fpm-request-smuggling", variant)
            with self.subTest(variant=variant), workspace() as work:
                result = module.run(payload)
                self.assertEqual(result["status"], 200)
                log = (work / "fpm-executed.log").read_text(encoding="utf-8").splitlines()
                if variant == "vulnerable":
                    self.assertEqual(log, ["/var/www/public.php", "/var/www/admin.php"])
                else:
                    self.assertEqual(log, ["/var/www/public.php"])


if __name__ == "__main__":
    unittest.main()
