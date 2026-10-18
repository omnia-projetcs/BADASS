"""Observe authenticated mutations, bounded inflation and session lifecycle."""
import base64
from contextlib import closing
import hashlib
import hmac
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import zlib

from test_exploitdb_cases import invoke, load


def invoices():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE invoices(id INTEGER PRIMARY KEY, total INTEGER, paid INTEGER)")
    db.executemany("INSERT INTO invoices VALUES (?, ?, 0)", [(1, 120), (2, 250)])
    db.commit()
    return db


def signature(body, key):
    return "sha256=" + hmac.new(key, body, hashlib.sha256).hexdigest()


class WebhookSignatureTests(unittest.TestCase):
    def test_tampered_body_updates_actual_invoice_only_before_repair(self):
        original, tampered = b'{"invoice":1,"amount":120}', b'{"invoice":2,"amount":250}'
        key = bytes(range(32))
        for variant in ("vulnerable", "fixed"):
            module = load("webhook-signature", variant)
            with self.subTest(variant=variant), closing(invoices()) as db:
                self.assertEqual(module.handle(tampered, signature(original, key), key, db),
                                 {"status": 200, "invoice": 2} if variant == "vulnerable" else {"status": 401})
                self.assertEqual(db.execute("SELECT paid FROM invoices ORDER BY id").fetchall(),
                                 [(0,), (1,)] if variant == "vulnerable" else [(0,), (0,)])

    def test_fixed_checks_exact_bytes_including_whitespace_and_unicode(self):
        module = load("webhook-signature", "fixed")
        key = b"synthetic-independent-test-key-32"
        body = b'{ "invoice" : 1, "amount" : 120 }'
        with closing(invoices()) as db:
            self.assertEqual(module.handle(body, signature(body, key), key, db), {"status": 200, "invoice": 1})
            db.execute("UPDATE invoices SET paid = 0")
            db.commit()
            canonical = b'{"invoice":1,"amount":120}'
            self.assertEqual(module.handle(canonical, signature(body, key), key, db), {"status": 401})
            self.assertEqual(db.execute("SELECT SUM(paid) FROM invoices").fetchone(), (0,))
            # Escaped names remain legitimate JSON when the exact bytes were signed.
            escaped = br'{"\u0069nvoice":2,"amount":250}'
            self.assertEqual(module.handle(escaped, signature(escaped, key), key, db), {"status": 200, "invoice": 2})

    def test_fixed_rejects_wrong_key_before_parsing_or_writing(self):
        module = load("webhook-signature", "fixed")
        body, key = b'{"invoice":1,"amount":120}', bytes(range(32))
        with closing(invoices()) as db, patch.object(module.json, "loads", side_effect=AssertionError("parsed unauthenticated body")):
            self.assertEqual(module.handle(body, signature(body, b"X" * 32), key, db), {"status": 401})
            self.assertEqual(db.execute("SELECT SUM(paid) FROM invoices").fetchone(), (0,))


class DecompressionBudgetTests(unittest.TestCase):
    def test_actual_output_file_respects_fixed_limit_including_binary_data(self):
        for variant in ("vulnerable", "fixed"):
            for data in (b"", b"x", bytes(range(256)) * 4, b"X" * 1025, b"X" * 16384):
                with self.subTest(variant=variant, size=len(data)), tempfile.TemporaryDirectory() as directory:
                    request = {"payload": base64.b64encode(zlib.compress(data)).decode("ascii")}
                    result = invoke(directory, "decompression-amplification", variant, request)
                    target = Path(directory) / "expanded.bin"
                    if variant == "fixed" and len(data) > 1024:
                        self.assertEqual(result, {"status": 413})
                        self.assertFalse(target.exists())
                    else:
                        self.assertEqual(result, {"status": 201, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
                        self.assertEqual(target.read_bytes(), data)

    def test_fixed_decoder_never_materializes_the_whole_expansion(self):
        module = load("decompression-amplification", "fixed")
        decoder_factory = zlib.decompressobj
        observed = []

        class ObservedDecoder:
            def __init__(self):
                self.decoder = decoder_factory()

            def decompress(self, data, max_length=0):
                self_outer.assertGreater(max_length, 0, "unbounded decoder allocation")
                self_outer.assertLessEqual(max_length, 1025)
                output = self.decoder.decompress(data, max_length)
                observed.append(len(output))
                return output

            def __getattr__(self, name):
                return getattr(self.decoder, name)

        self_outer = self
        with patch.object(module.zlib, "decompressobj", ObservedDecoder), self.assertRaises(OverflowError):
            module.unpack(zlib.compress(b"A" * 16384))
        self.assertEqual(observed, [1025])

    def test_truncated_corrupt_and_concatenated_streams_publish_nothing(self):
        valid = zlib.compress(b"valid")
        streams = (valid[:-1], b"invalid", valid + b"trailing", valid + valid)
        for variant in ("vulnerable", "fixed"):
            for packed in streams:
                with self.subTest(variant=variant, packed=packed), tempfile.TemporaryDirectory() as directory:
                    result = invoke(directory, "decompression-amplification", variant,
                                    {"payload": base64.b64encode(packed).decode("ascii")})
                    self.assertEqual(result, {"status": 400})
                    self.assertFalse((Path(directory) / "expanded.bin").exists())


class SessionLifecycleTests(unittest.TestCase):
    def test_logout_revocation_survives_reopen_and_blocks_actual_private_report(self):
        for variant in ("vulnerable", "fixed"):
            module = load("session-expiration", variant)
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "sessions.sqlite"
                with closing(sqlite3.connect(path)) as db:
                    token = module.initialize(db)
                    db.execute("UPDATE reports SET body = 'CHANGED_PRIVATE_REPORT'")
                    db.commit()
                    self.assertEqual(module.dispatch(db, token, "read", module.NOW),
                                     {"status": 200, "report": "CHANGED_PRIVATE_REPORT"})
                    self.assertEqual(module.dispatch(db, token, "logout", module.NOW + 1), {"status": 204})
                with closing(sqlite3.connect(path)) as db:
                    self.assertEqual(db.execute("SELECT revoked FROM sessions").fetchone(), (1,))
                    self.assertEqual(module.dispatch(db, token, "read", module.NOW + 2),
                                     {"status": 200, "report": "CHANGED_PRIVATE_REPORT"} if variant == "vulnerable" else {"status": 401})

    def test_fixed_expiry_boundary_denies_before_reading_report(self):
        module = load("session-expiration", "fixed")
        with closing(sqlite3.connect(":memory:")) as db:
            token = module.initialize(db)
            self.assertEqual(module.dispatch(db, token, "read", module.NOW + 59)["status"], 200)
            statements = []
            db.set_trace_callback(statements.append)
            for now in (module.NOW + 60, module.NOW + 61):
                self.assertEqual(module.dispatch(db, token, "read", now), {"status": 401})
            self.assertFalse(any("FROM reports" in sql for sql in statements))

    def test_unknown_token_cannot_read_or_revoke_existing_session(self):
        for variant in ("vulnerable", "fixed"):
            module = load("session-expiration", variant)
            with self.subTest(variant=variant), closing(sqlite3.connect(":memory:")) as db:
                token = module.initialize(db)
                for operation in ("read", "logout"):
                    self.assertEqual(module.dispatch(db, "UNKNOWN", operation, module.NOW), {"status": 401})
                self.assertEqual(db.execute("SELECT revoked FROM sessions").fetchone(), (0,))
                self.assertEqual(module.dispatch(db, token, "read", module.NOW)["status"], 200)


if __name__ == "__main__":
    unittest.main()
