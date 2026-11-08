"""Repair mutations must be rejected without modifying trusted hash functions."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from repair_oracles import evaluate


def load_fixture(path):
    spec = importlib.util.spec_from_file_location("fixture_" + uuid4().hex, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepairOracleTests(unittest.TestCase):
    def original(self, case, variant="fixed"):
        return load_fixture(ROOT / "labs" / case / variant / "main.py")

    def mutation(self, case, transform):
        source = (ROOT / "labs" / case / "fixed/main.py").read_text()
        changed = transform(source)
        self.assertNotEqual(source, changed, "Mutation did not change the fixture")
        directory = tempfile.TemporaryDirectory(prefix="badass-mutant-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "main.py"
        path.write_text(changed)
        return load_fixture(path)

    def test_both_token_variants_preserve_real_token_validation(self):
        expected = {
            "issued_token_usable": True, "wrong_token_rejected": True,
            "consumed_token_accepted": True, "replay_rejected": True,
            "token_removed": True, "unrelated_token_preserved": True,
        }
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant):
                self.assertEqual(evaluate("reset_token", self.original("python/predictable-token", variant), "alice"), expected)

    def test_consumption_without_invalidation_is_detected(self):
        module = self.mutation("python/predictable-token", lambda source: source.replace("    del tokens[account]\n", ""))
        observed = evaluate("reset_token", module, "alice")
        self.assertTrue(observed["consumed_token_accepted"])
        self.assertFalse(observed["replay_rejected"])
        self.assertFalse(observed["token_removed"])

    def test_public_guess_is_accepted_only_by_vulnerable_token_store(self):
        for variant, accepted in (("vulnerable", True), ("fixed", False)):
            observed = evaluate("reset_token", self.original("python/predictable-token", variant),
                                "alice", {"scenario": "public_guess"})
            self.assertTrue(observed["issued_token_usable"])
            self.assertIs(observed["public_guess_accepted"], accepted)

    def test_constant_token_mutation_is_detected(self):
        case = "python/predictable-token"
        module = self.mutation(case, lambda source: source.replace("secrets.token_hex(32)", '"0" * 64'))
        observed = evaluate("reset_token", module, "alice", {"scenario": "repeated_issuance"})
        self.assertEqual(observed, {"issued_tokens_usable": True, "distinct_tokens": False})
        self.assertEqual(evaluate("reset_token", self.original(case), "alice", {"scenario": "repeated_issuance"}),
                         {"issued_tokens_usable": True, "distinct_tokens": True})

    def test_vulnerable_password_store_is_functional_but_fails_kdf_contract(self):
        module = self.original("python/weak-password-hash", "vulnerable")
        self.assertEqual(evaluate("password_hash", module, "correct-horse"),
                         {"correct_password_works": True, "wrong_password_rejected": True})
        self.assertEqual(evaluate("password_hash", module, "correct-horse", {"scenario": "storage_profile"}),
                         {"correct_password_works": True, "valid_scrypt_record": False})

    def test_real_fixed_password_record_is_independently_verified(self):
        module = self.original("python/weak-password-hash")
        self.assertEqual(evaluate("password_hash", module, "correct-horse", {"scenario": "storage_profile"}),
                         {"correct_password_works": True, "valid_scrypt_record": True})

    def test_md5_with_false_scrypt_metadata_is_detected(self):
        original_scrypt = hashlib.scrypt

        def weaken(source):
            # Real source substitution in an isolated module, not a monkeypatch
            # of the shared hashlib module. Keep digest length and KDF labels.
            source = source.replace("hashlib.scrypt(", "_fast_digest(")
            return source + "\n\ndef _fast_digest(encoded, **ignored):\n    return hashlib.md5(encoded).digest() * 2\n"

        module = self.mutation("python/weak-password-hash", weaken)
        record = module.hash_password("correct-horse")
        self.assertEqual(record["algorithm"], "scrypt")
        self.assertEqual(len(record["digest"]), 64)
        self.assertEqual(evaluate("password_hash", module, "correct-horse", {"scenario": "storage_profile"}),
                         {"correct_password_works": True, "valid_scrypt_record": False})
        self.assertIs(hashlib.scrypt, original_scrypt)

    def test_constant_salt_mutation_is_detected(self):
        module = self.mutation(
            "python/weak-password-hash",
            lambda source: source.replace("secrets.token_bytes(SALT_BYTES)", 'b"\\0" * SALT_BYTES'),
        )
        self.assertTrue(evaluate("password_hash", module, "correct-horse", {"scenario": "storage_profile"})["valid_scrypt_record"])
        self.assertEqual(evaluate("password_hash", module, "correct-horse", {"scenario": "independent_salts"}),
                         {"records_usable": True, "distinct_salts": False, "distinct_digests": False})
        expected = {"records_usable": True, "distinct_salts": True, "distinct_digests": True}
        self.assertEqual(evaluate("password_hash", self.original("python/weak-password-hash"),
                                 "correct-horse", {"scenario": "independent_salts"}), expected)

    def test_verifier_accepting_wrong_password_is_detected(self):
        def accept_everything(source):
            return source.split("def verify_password(")[0] + "def verify_password(password, record):\n    return True\n"

        module = self.mutation("python/weak-password-hash", accept_everything)
        self.assertEqual(evaluate("password_hash", module, "correct-horse"),
                         {"correct_password_works": True, "wrong_password_rejected": False})

    def test_session_rotation_preserves_authenticated_state(self):
        for variant, rotated in (("vulnerable", False), ("fixed", True)):
            result = evaluate("session_rotation", self.original("python/session-fixation", variant),
                              "attacker-known-id", {"scenario": "rotation"})
            self.assertTrue(result["new_session_authenticated"])
            self.assertTrue(result["unrelated_session_preserved"])
            self.assertIs(result["id_rotated"], rotated)
            self.assertIs(result["old_session_removed"], rotated)
            self.assertIs(result["old_session_authenticated"], not rotated)

    def test_both_variants_support_real_logout(self):
        expected = {
            "new_session_authenticated": True, "unrelated_session_preserved": True,
            "logout_succeeded": True, "logged_out_session_rejected": True,
            "logged_out_session_removed": True,
        }
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant):
                self.assertEqual(evaluate("session_rotation", self.original("python/session-fixation", variant),
                                          "old-id", {"scenario": "login_logout"}), expected)

    def test_logout_without_invalidating_session_is_detected(self):
        module = self.mutation("python/session-fixation", lambda source: source.replace("    del sessions[session_id]\n", ""))
        observed = evaluate("session_rotation", module, "old-id", {"scenario": "login_logout"})
        self.assertTrue(observed["logout_succeeded"])
        self.assertFalse(observed["logged_out_session_rejected"])
        self.assertFalse(observed["logged_out_session_removed"])

    def test_missing_authenticated_session_mutation_is_detected(self):
        module = self.mutation("python/session-fixation",
                               lambda source: source.replace("    sessions[new_id] = principal\n", ""))
        self.assertEqual(evaluate("session_rotation", module, "attacker-known-id"),
                         {"new_session_authenticated": False, "unrelated_session_preserved": True})

    def test_removing_unrelated_sessions_is_detected(self):
        module = self.mutation("python/session-fixation",
                               lambda source: source.replace("sessions.pop(old_id, None)", "sessions.clear()"))
        self.assertEqual(evaluate("session_rotation", module, "attacker-known-id"),
                         {"new_session_authenticated": True, "unrelated_session_preserved": False})

    def test_disabled_operations_cannot_pass_functional_scenarios(self):
        cases = (
            ("python/predictable-token", "reset_token", "def issue_reset_token(account, tokens):", "alice"),
            ("python/weak-password-hash", "password_hash", "def hash_password(password):", "correct-horse"),
            ("python/session-fixation", "session_rotation", "def login(old_id, principal, sessions):", "old-id"),
        )
        for case, oracle, signature, value in cases:
            with self.subTest(case=case):
                baseline = evaluate(oracle, self.original(case), value)
                module = self.mutation(case, lambda source: source.replace(signature, signature + "\n    return None", 1))
                self.assertEqual(evaluate(oracle, module, value), "DENIED")
                self.assertNotEqual(baseline, "DENIED")

    def test_invalid_trusted_oracle_configuration_is_rejected(self):
        module = self.original("python/predictable-token")
        with self.assertRaises(ValueError):
            evaluate("unknown", module, "alice")
        with self.assertRaises(ValueError):
            evaluate("reset_token", module, "alice", [])
        with self.assertRaises(ValueError):
            evaluate("reset_token", module, "alice", {"scenario": "unknown"})


class InvokeProtocolTests(unittest.TestCase):
    def invoke(self, source, value, *options):
        return subprocess.run([sys.executable, str(ROOT / "tools/invoke.py"), str(source),
                               json.dumps(value), *options], capture_output=True, text=True, timeout=10)

    def test_legacy_run_interface_is_unchanged(self):
        result = self.invoke(ROOT / "labs/python/xss/fixed/main.py", "<b>hello</b>")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), "<p>&lt;b&gt;hello&lt;/b&gt;</p>")

    def test_named_oracle_receives_trusted_context(self):
        result = self.invoke(ROOT / "labs/python/session-fixation/fixed/main.py", "old-id",
                             "--oracle", "session_rotation", "--context",
                             json.dumps({"scenario": "rotation", "principal": "charlie"}))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "new_session_authenticated": True, "unrelated_session_preserved": True,
            "id_rotated": True, "old_session_removed": True, "old_session_authenticated": False,
        })

    def test_context_without_oracle_is_rejected_before_loading_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "main.py"
            source.write_text('raise RuntimeError("candidate should not load")\n')
            result = self.invoke(source, None, "--context", "{}")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--context requires --oracle", result.stderr)
        self.assertNotIn("candidate should not load", result.stderr)

    def test_unknown_oracle_is_rejected_before_loading_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "main.py"
            source.write_text('raise RuntimeError("candidate should not load")\n')
            result = self.invoke(source, None, "--oracle", "unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown trusted oracle", result.stderr)
        self.assertNotIn("candidate should not load", result.stderr)


if __name__ == "__main__":
    unittest.main()
