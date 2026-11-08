"""Observe parser disagreement, canonical paths and persisted recovery state."""
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest

from test_exploitdb_cases import load


def payment_database():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE wallet(id INTEGER PRIMARY KEY, balance INTEGER)")
    db.execute("INSERT INTO wallet VALUES (1, 5000)")
    db.execute("CREATE TABLE payments(amount INTEGER, recipient TEXT)")
    db.commit()
    return db


class ParserConflictTests(unittest.TestCase):
    def test_duplicate_and_escaped_keys_change_real_debit_only_before_repair(self):
        for variant in ("vulnerable", "fixed"):
            module = load("json-parser-conflict", variant)
            for raw in ('{"amount":7,"amount":713,"recipient":"vendor"}',
                        r'{"amount":7,"\u0061mount":713,"recipient":"vendor"}'):
                with self.subTest(variant=variant, raw=raw), closing(payment_database()) as db:
                    result = module.transfer(raw, db)
                    self.assertEqual(result, {"status": 201, "amount": 713} if variant == "vulnerable" else {"status": 400})
                    self.assertEqual(db.execute("SELECT balance FROM wallet").fetchone()[0],
                                     4287 if variant == "vulnerable" else 5000)
                    self.assertEqual(db.execute("SELECT amount FROM payments").fetchall(),
                                     [(713,)] if variant == "vulnerable" else [])

    def test_fixed_keeps_ordinary_payments_and_rejects_ambiguous_or_invalid_values(self):
        module = load("json-parser-conflict", "fixed")
        with closing(payment_database()) as db:
            self.assertEqual(module.transfer('{"amount":93,"recipient":"vendor"}', db),
                             {"status": 201, "amount": 93})
            for raw in ('{"amount":1,"amount":1,"recipient":"vendor"}',
                        '{"amount":true,"recipient":"vendor"}',
                        '{"amount":NaN,"recipient":"vendor"}',
                        '{"amount":101,"recipient":"vendor"}',
                        '{"amount":1,"recipient":"vendor","extra":{"x":1,"x":2}}'):
                self.assertEqual(module.transfer(raw, db), {"status": 400})
            self.assertEqual(db.execute("SELECT balance FROM wallet").fetchone(), (4907,))
            self.assertEqual(db.execute("SELECT amount FROM payments").fetchall(), [(93,)])


class UnicodePathTests(unittest.TestCase):
    def test_compatibility_normalization_can_create_traversal_after_validation(self):
        for variant in ("vulnerable", "fixed"):
            module = load("unicode-path-validation", variant)
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "public"
                root.mkdir()
                (root.parent / "private.txt").write_text("CHANGED_PRIVATE_BYTES", encoding="utf-8")
                for name in ("．．／private.txt", "﹒﹒／private.txt"):
                    self.assertEqual(module.read_public(name, root),
                                     {"status": 200, "text": "CHANGED_PRIVATE_BYTES"} if variant == "vulnerable" else {"status": 400})

    def test_fixed_preserves_compatible_public_names_and_confines_symlinks(self):
        module = load("unicode-path-validation", "fixed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "public"
            root.mkdir()
            (root / "note.txt").write_text("PUBLIC é", encoding="utf-8")
            outside = root.parent / "secret.txt"
            outside.write_text("SECRET")
            (root / "link.txt").symlink_to(outside)
            for name in ("note.txt", "ｎｏｔｅ．ｔｘｔ"):
                self.assertEqual(module.read_public(name, root), {"status": 200, "text": "PUBLIC é"})
            for name in ("link.txt", "ｌｉｎｋ．ｔｘｔ", "../secret.txt", "．．／secret.txt", str(outside)):
                self.assertEqual(module.read_public(name, root), {"status": 400})


class RecoveryReplayTests(unittest.TestCase):
    def test_replay_cannot_replace_the_first_new_password_after_repair(self):
        for variant in ("vulnerable", "fixed"):
            module = load("password-reset-replay", variant)
            with self.subTest(variant=variant), closing(sqlite3.connect(":memory:")) as db:
                token = module.initialize(db)
                self.assertEqual(module.reset_password(db, token, "Owner-NEW-password", module.NOW), {"status": 200})
                self.assertEqual(module.reset_password(db, token, "Replay-NEW-password", module.NOW + 1),
                                 {"status": 200 if variant == "vulnerable" else 403})
                self.assertEqual(module.password_matches(db, "Owner-NEW-password"), variant == "fixed")
                self.assertEqual(module.password_matches(db, "Replay-NEW-password"), variant == "vulnerable")
                self.assertFalse(module.password_matches(db, module.INITIAL_PASSWORD))
                self.assertEqual(db.execute("SELECT used FROM reset_tokens").fetchone()[0], int(variant == "fixed"))

    def test_unknown_expired_and_invalid_inputs_do_not_change_credentials(self):
        for variant in ("vulnerable", "fixed"):
            module = load("password-reset-replay", variant)
            with self.subTest(variant=variant), closing(sqlite3.connect(":memory:")) as db:
                token = module.initialize(db)
                for credential, password, now, status in (
                    ("unknown", "New-password", module.NOW, 403),
                    (token, "New-password", module.NOW + 100, 403),
                    (token, "short", module.NOW, 400),
                    (token, "New-password", True, 400),
                ):
                    self.assertEqual(module.reset_password(db, credential, password, now), {"status": status})
                    self.assertTrue(module.password_matches(db, module.INITIAL_PASSWORD))
                    self.assertEqual(db.execute("SELECT used FROM reset_tokens").fetchone(), (0,))
                self.assertEqual(module.reset_password(db, token, "Valid-new-password", module.NOW + 99), {"status": 200})

    def test_fixed_rolls_back_token_consumption_when_password_write_fails(self):
        module = load("password-reset-replay", "fixed")
        with closing(sqlite3.connect(":memory:")) as db:
            token = module.initialize(db)
            db.execute("CREATE TRIGGER reject_password BEFORE UPDATE ON accounts BEGIN SELECT RAISE(ABORT, 'write failed'); END")
            with self.assertRaises(sqlite3.IntegrityError):
                module.reset_password(db, token, "New-password", module.NOW)
            self.assertEqual(db.execute("SELECT used FROM reset_tokens").fetchone(), (0,))
            self.assertTrue(module.password_matches(db, module.INITIAL_PASSWORD))
            db.execute("DROP TRIGGER reject_password")
            self.assertEqual(module.reset_password(db, token, "Retry-password", module.NOW), {"status": 200})

    def test_concurrent_connections_can_consume_fixed_token_only_once(self):
        module = load("password-reset-replay", "fixed")
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "recovery.sqlite"
            with closing(sqlite3.connect(database)) as db:
                token = module.initialize(db)
            barrier = threading.Barrier(2, timeout=3)
            results, failures = {}, []

            def reset(password):
                try:
                    with closing(sqlite3.connect(database, timeout=5)) as db:
                        barrier.wait()
                        results[password] = module.reset_password(db, token, password, module.NOW)["status"]
                except BaseException as error:
                    failures.append(error)

            threads = [threading.Thread(target=reset, args=(password,), daemon=True)
                       for password in ("First-password", "Second-password")]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(6)
            self.assertFalse(any(thread.is_alive() for thread in threads))
            self.assertEqual(failures, [])
            self.assertEqual(sorted(results.values()), [200, 403])
            with closing(sqlite3.connect(database)) as db:
                for password, status in results.items():
                    self.assertEqual(module.password_matches(db, password), status == 200)
                self.assertEqual(db.execute("SELECT used FROM reset_tokens").fetchone(), (1,))


if __name__ == "__main__":
    unittest.main()
