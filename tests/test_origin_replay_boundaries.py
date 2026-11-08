"""Observe origin policy and replay effects in both runtime implementations."""
import hashlib
import hmac
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from test_cross_language_boundaries import invoke, source
from test_exploitdb_cases import load


def require_runtime(language):
    if language == "node" and not shutil.which("node"):
        raise unittest.SkipTest("Node.js unavailable")


def node_call(slug, variant, script, payload):
    process = subprocess.run(["node", "-e", script, str(source("node", slug, variant)), json.dumps(payload)],
                             text=True, capture_output=True, check=True, timeout=10)
    return json.loads(process.stdout)


def process_messages(language, variant, messages, balance=400):
    key = bytes(range(32))
    if language == "python":
        processor = load("signed-action-replay", variant).Processor(key, balance)
        results = []
        for message in messages:
            if "credit" in message:
                processor.balance += message["credit"]
            else:
                results.append(processor.process(bytes.fromhex(message["body"]), message["tag"], message["now"]))
        return {"results": results, "balance": processor.balance, "accepted": processor.accepted}
    script = """
const fixture = require(process.argv[1]);
const input = JSON.parse(process.argv[2]);
const processor = new fixture.Processor(Buffer.from(input.key, 'hex'), input.balance);
const results = [];
for (const message of input.messages) {
    if ('credit' in message) processor.balance += message.credit;
    else results.push(processor.process(Buffer.from(message.body, 'hex'), message.tag, message.now));
}
process.stdout.write(JSON.stringify({results, balance: processor.balance, accepted: processor.accepted}));
"""
    return node_call("signed-action-replay", variant, script, {"key": key.hex(), "balance": balance, "messages": messages})


def signed_message(identifier="delivery-x", amount=37, expires=1060, now=1000):
    body = json.dumps({"id": identifier, "amount": amount, "expires": expires}, separators=(",", ":")).encode()
    return {"body": body.hex(), "tag": hmac.new(bytes(range(32)), body, hashlib.sha256).hexdigest(), "now": now}


class OriginBoundaryTests(unittest.TestCase):
    def test_unrelated_origins_receive_private_response_only_before_repair(self):
        for language in ("python", "node"):
            for variant in ("vulnerable", "fixed"):
                for origin in ("https://alpha-example.test", "https://alpha.example-test", "https://alphaxexampleytest"):
                    with self.subTest(language=language, variant=variant, origin=origin), tempfile.TemporaryDirectory() as work:
                        require_runtime(language)
                        result = invoke(language, "regex-origin", variant, origin, work)
                        artifact = Path(work) / "cors-response.json"
                        if variant == "vulnerable":
                            self.assertEqual(result["status"], 200)
                            self.assertEqual(result["headers"]["Access-Control-Allow-Origin"], origin)
                            self.assertEqual(result["headers"]["Access-Control-Allow-Credentials"], "true")
                            self.assertEqual(result["body"], "LAB_PRIVATE_PROFILE")
                            self.assertEqual(json.loads(artifact.read_text()), result)
                        else:
                            self.assertEqual(result, {"status": 403})
                            self.assertFalse(artifact.exists())

    def test_fixed_preserves_approved_origins_and_changed_private_data(self):
        for language in ("python", "node"):
            with self.subTest(language=language):
                require_runtime(language)
                origin = "https://research.example.test"
                if language == "python":
                    result = load("regex-origin", "fixed").response(origin, "CHANGED_PROFILE")
                else:
                    script = "const m=require(process.argv[1]); const p=JSON.parse(process.argv[2]); process.stdout.write(JSON.stringify(m.response(p.origin,p.secret)));"
                    result = node_call("regex-origin", "fixed", script, {"origin": origin, "secret": "CHANGED_PROFILE"})
                self.assertEqual(result, {"status": 200, "headers": {"Access-Control-Allow-Origin": origin,
                                 "Access-Control-Allow-Credentials": "true"}, "body": "CHANGED_PROFILE"})

    def test_fixed_rejects_suffixes_userinfo_and_header_controls(self):
        cases = [("https://alpha.example.test.evil.test", 403), ("https://alpha.example.test@evil.test", 403),
                 ("http://alpha.example.test", 403), ("https://alpha.example.test\n", 400),
                 ("https://alpha.example.test\r\nX-Evil: yes", 400), ("https://alpha.example.test/path", 403)]
        for language in ("python", "node"):
            for origin, status in cases:
                with self.subTest(language=language, origin=origin), tempfile.TemporaryDirectory() as work:
                    require_runtime(language)
                    self.assertEqual(invoke(language, "regex-origin", "fixed", origin, work), {"status": status})
                    self.assertFalse((Path(work) / "cors-response.json").exists())


class ReplayBoundaryTests(unittest.TestCase):
    def test_identical_captured_bytes_cannot_authorize_second_fixed_debit(self):
        message = signed_message()
        for language in ("python", "node"):
            for variant in ("vulnerable", "fixed"):
                with self.subTest(language=language, variant=variant):
                    require_runtime(language)
                    result = process_messages(language, variant, [message, message])
                    count = 2 if variant == "vulnerable" else 1
                    self.assertEqual(result["results"], [{"status": 200}, {"status": 200 if count == 2 else 409}])
                    self.assertEqual(result["balance"], 400 - count * 37)
                    self.assertEqual(result["accepted"], [{"id": "delivery-x", "amount": 37}] * count)

    def test_tampering_and_expiry_do_not_consume_valid_action(self):
        valid = signed_message()
        tampered = signed_message(amount=38)
        tampered["tag"] = valid["tag"]
        expired = signed_message(expires=1000)
        for language in ("python", "node"):
            with self.subTest(language=language):
                require_runtime(language)
                result = process_messages(language, "fixed", [tampered, expired, valid])
                self.assertEqual(result["results"], [{"status": 401}, {"status": 401}, {"status": 200}])
                self.assertEqual(result["balance"], 363)
                self.assertEqual(len(result["accepted"]), 1)

    def test_failed_debit_does_not_burn_id_and_distinct_ids_remain_usable(self):
        first, second = signed_message(), signed_message(identifier="delivery-y", amount=11)
        for language in ("python", "node"):
            with self.subTest(language=language):
                require_runtime(language)
                result = process_messages(language, "fixed", [first, {"credit": 100}, first, second], balance=20)
                self.assertEqual(result["results"], [{"status": 402}, {"status": 200}, {"status": 200}])
                self.assertEqual(result["balance"], 72)
                self.assertEqual(result["accepted"], [{"id": "delivery-x", "amount": 37}, {"id": "delivery-y", "amount": 11}])

    def test_replayed_scenario_has_only_one_fixed_entry_in_actual_ledger_file(self):
        request = {"actions": [{"id": "event-1", "amount": 120, "signature": "valid", "at": 1000}] * 2}
        for language in ("python", "node"):
            for variant in ("vulnerable", "fixed"):
                with self.subTest(language=language, variant=variant), tempfile.TemporaryDirectory() as work:
                    require_runtime(language)
                    result = invoke(language, "signed-action-replay", variant, request, work)
                    count = 2 if variant == "vulnerable" else 1
                    self.assertEqual(result["balance"], 1000 - count * 120)
                    ledger = json.loads((Path(work) / "ledger.json").read_text())
                    self.assertEqual(ledger, {"balance": result["balance"], "accepted": [{"id": "event-1", "amount": 120}] * count})


if __name__ == "__main__":
    unittest.main()
