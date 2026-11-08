"""Verify the same authentication and pricing boundaries in Python and Node.js."""
import hashlib
import hmac
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_exploitdb_cases import load


ROOT = Path(__file__).resolve().parents[1]


def source(language, slug, variant):
    return ROOT / "labs" / language / slug / variant / ("main.py" if language == "python" else "main.js")


def invoke(language, slug, variant, request, work):
    path = source(language, slug, variant)
    command = ([sys.executable, str(ROOT / "tools/invoke.py"), str(path)] if language == "python"
               else ["node", str(path)])
    result = subprocess.run(command + [json.dumps(request)], cwd=work, text=True,
                            capture_output=True, check=True, timeout=10)
    return json.loads(result.stdout)


class CrossLanguageBoundaryTests(unittest.TestCase):
    def languages(self):
        yield "python"
        if shutil.which("node"):
            yield "node"

    def verify_tags(self, language, variant, body, key, tags):
        if language == "python":
            module = load("partial-signature", variant)
            return [module.verify(body, tag, key) for tag in tags]
        script = """
const fixture = require(process.argv[1]);
const input = JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify(input.tags.map(tag => fixture.verify(
    Buffer.from(input.body, 'hex'), tag, Buffer.from(input.key, 'hex')))));
"""
        result = subprocess.run(["node", "-e", script, str(source(language, "partial-signature", variant)),
                                 json.dumps({"body": body.hex(), "key": key.hex(), "tags": tags})],
                                text=True, capture_output=True, check=True, timeout=10)
        return json.loads(result.stdout)

    def test_full_tag_passes_but_empty_and_one_byte_tags_only_pass_before_repair(self):
        body, key = b"CHANGED_SYNTHETIC_MESSAGE", bytes(range(32))
        correct = hmac.new(key, body, hashlib.sha256).hexdigest()
        tags = [correct, ""] + [f"{byte:02x}" for byte in range(256)]
        for language in self.languages():
            for variant in ("vulnerable", "fixed"):
                with self.subTest(language=language, variant=variant):
                    results = self.verify_tags(language, variant, body, key, tags)
                    self.assertTrue(results[0])
                    self.assertEqual(results[1], variant == "vulnerable")
                    self.assertEqual(sum(results[2:]), 1 if variant == "vulnerable" else 0)

    def test_invalid_or_extended_tags_are_rejected_without_exceptions(self):
        body, key = b"message", b"K" * 32
        correct = hmac.new(key, body, hashlib.sha256).hexdigest()
        tags = [correct + "0", correct + "\n", correct + "\r", "\n", "é", None, 123, "g" * 64]
        for language in self.languages():
            for variant in ("vulnerable", "fixed"):
                with self.subTest(language=language, variant=variant):
                    self.assertEqual(self.verify_tags(language, variant, body, key, tags), [False] * len(tags))

    def test_unauthenticated_empty_tag_can_publish_only_in_vulnerable_variant(self):
        for language in self.languages():
            for variant in ("vulnerable", "fixed"):
                with self.subTest(language=language, variant=variant), tempfile.TemporaryDirectory() as work:
                    body = "FORGED é MESSAGE"
                    result = invoke(language, "partial-signature", variant, {"body": body, "signature": "empty"}, work)
                    target = Path(work) / "verified-message.txt"
                    if variant == "vulnerable":
                        self.assertEqual(result, {"status": 201, "bytes": len(body.encode())})
                        self.assertEqual(target.read_bytes(), body.encode())
                    else:
                        self.assertEqual(result, {"status": 401})
                        self.assertFalse(target.exists())

    def test_matching_full_tag_preserves_empty_and_unicode_messages(self):
        for language in self.languages():
            for variant in ("vulnerable", "fixed"):
                for body in ("", "Signed message é\n"):
                    with self.subTest(language=language, variant=variant, body=body), tempfile.TemporaryDirectory() as work:
                        result = invoke(language, "partial-signature", variant, {"body": body, "signature": "valid"}, work)
                        self.assertEqual(result, {"status": 201, "bytes": len(body.encode())})
                        self.assertEqual((Path(work) / "verified-message.txt").read_bytes(), body.encode())

    def test_tampered_price_changes_actual_receipt_only_before_repair(self):
        for language in self.languages():
            for variant in ("vulnerable", "fixed"):
                with self.subTest(language=language, variant=variant), tempfile.TemporaryDirectory() as work:
                    result = invoke(language, "client-price", variant,
                                    {"product": "lamp", "quantity": 3, "unit_price": 1}, work)
                    total = 3 if variant == "vulnerable" else 750
                    self.assertEqual(result, {"status": 201, "total": total, "remaining": 1000 - total})
                    receipt = json.loads((Path(work) / "order.json").read_text())
                    self.assertEqual(receipt, {"product": "lamp", "quantity": 3,
                                     "unit_price": 1 if variant == "vulnerable" else 250,
                                     "total": total, "remaining": 1000 - total})

    def test_fixed_uses_changed_server_catalog_and_balance(self):
        request = {"product": "custom", "quantity": 2, "unit_price": 1}
        expected = {"status": 201, "receipt": {"product": "custom", "quantity": 2,
                    "unit_price": 499, "total": 998, "remaining": 2}}
        for language in self.languages():
            with self.subTest(language=language):
                if language == "python":
                    module = load("client-price", "fixed")
                    results = [module.quote(request, {"custom": 499}, balance) for balance in (1000, 997)]
                else:
                    script = """
const fixture = require(process.argv[1]);
const request = JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify([1000, 997].map(balance => fixture.quote(request, {custom: 499}, balance))));
"""
                    process = subprocess.run(["node", "-e", script, str(source(language, "client-price", "fixed")), json.dumps(request)],
                                             text=True, capture_output=True, check=True, timeout=10)
                    results = json.loads(process.stdout)
                self.assertEqual(results, [expected, {"status": 402}])

    def test_rejected_orders_do_not_publish_receipts(self):
        requests = [({"product": "__proto__", "quantity": 1, "unit_price": 1}, 404),
                    ({"product": "lamp", "quantity": 5, "unit_price": 250}, 402),
                    ({"product": "book", "quantity": True, "unit_price": 120}, 400),
                    ({"product": "book", "quantity": 1.5, "unit_price": 120}, 400)]
        for language in self.languages():
            for variant in ("vulnerable", "fixed"):
                for request, status in requests:
                    with self.subTest(language=language, variant=variant, request=request), tempfile.TemporaryDirectory() as work:
                        self.assertEqual(invoke(language, "client-price", variant, request, work), {"status": status})
                        self.assertFalse((Path(work) / "order.json").exists())


if __name__ == "__main__":
    unittest.main()
