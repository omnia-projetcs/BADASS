"""Exercise complete signed resource scopes, session transitions and path ancestry."""
from copy import deepcopy
import hashlib
import hmac
import json
from pathlib import Path
import secrets
import tempfile
import unittest

from test_tenant_isolation import invoke, load, workspace


class SignedDownloadTests(unittest.TestCase):
    def test_real_signature_binds_complete_scope_only_in_fixed_variant(self):
        key = secrets.token_bytes(32)
        expires = 2_000_000_300
        for variant in ("vulnerable", "fixed"):
            module = load("tenant-signed-download", variant)
            with self.subTest(variant=variant):
                signature = module.sign("north", "report", expires, key)
                payload = ["download", "report", expires] if variant == "vulnerable" else ["download", "north", "report", expires]
                expected = hmac.new(key, json.dumps(payload, separators=(",", ":")).encode(), hashlib.sha256).hexdigest()
                self.assertEqual(signature, expected)
                self.assertEqual(module.redeem("north", "report", expires, signature, key)["status"], 200)
                result = module.redeem("south", "report", expires, signature, key)
                self.assertEqual(result, {"status": 200, "content": "LAB_SOUTH_SHARED_REPORT"} if variant == "vulnerable" else {"status": 403})

    def test_changed_key_id_expiry_and_expired_grant_are_denied(self):
        key = secrets.token_bytes(32)
        for variant in ("vulnerable", "fixed"):
            module = load("tenant-signed-download", variant)
            expires = module.NOW + 30
            signature = module.sign("north", "report", expires, key)
            calls = [
                ("north", "notes", expires, signature, key, module.NOW),
                ("north", "report", expires + 1, signature, key, module.NOW),
                ("north", "report", expires, signature, secrets.token_bytes(32), module.NOW),
                ("north", "report", expires, signature, key, expires),
                ("north", "report", expires, "not-a-signature", key, module.NOW),
            ]
            for arguments in calls:
                with self.subTest(variant=variant, arguments=arguments[:3]):
                    self.assertEqual(module.redeem(*arguments), {"status": 403})

    def test_fixed_scope_encoding_is_unambiguous_and_not_limited_to_known_tenants(self):
        module = load("tenant-signed-download", "fixed")
        key = secrets.token_bytes(32)
        expires = module.NOW + 30
        self.assertNotEqual(module.sign("ab", "c", expires, key), module.sign("a", "bc", expires, key))
        module.DOCUMENTS[("third", "report")] = "THIRD_ONLY"
        signature = module.sign("third", "report", expires, key)
        self.assertEqual(module.redeem("third", "report", expires, signature, key), {"status": 200, "content": "THIRD_ONLY"})
        self.assertEqual(module.redeem("north", "report", expires, signature, key), {"status": 403})


class SessionSwitchTests(unittest.TestCase):
    def test_downgrade_preserves_foreign_account_and_persists_current_role(self):
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant), workspace() as work:
                result = invoke(work, "tenant-session-switch", variant, {
                    "session": "LAB_ALICE_NORTH", "actions": [
                        {"action": "switch", "tenant": "south", "role": "admin"},
                        {"action": "disable", "account_id": "south-member"},
                    ]})
                state = json.loads((work / "session-state.json").read_text())
                self.assertEqual(result["events"][-1]["status"], 200 if variant == "vulnerable" else 403)
                self.assertEqual(state["session"]["role"], "admin" if variant == "vulnerable" else "viewer")
                self.assertEqual(state["session"]["tenant"], "south")
                self.assertEqual(state["accounts"]["south-member"]["active"], variant == "fixed")
                self.assertTrue(state["accounts"]["north-member"]["active"])

    def test_rejected_switch_does_not_change_session_and_valid_switch_updates_role(self):
        module = load("tenant-session-switch", "fixed")
        session = {"subject": "alice", "tenant": "south", "role": "viewer"}
        accounts = deepcopy(module.ACCOUNTS)
        before = dict(session)
        self.assertEqual(module.apply({"action": "switch", "tenant": "unjoined"}, session, accounts), {"status": 403})
        self.assertEqual(session, before)
        self.assertEqual(module.apply({"action": "switch", "tenant": "north"}, session, accounts)["status"], 200)
        self.assertEqual(session, {"subject": "alice", "tenant": "north", "role": "admin"})
        self.assertEqual(module.apply({"action": "disable", "account_id": "north-member"}, session, accounts)["status"], 200)
        self.assertTrue(accounts["south-member"]["active"])


class StorageAncestryTests(unittest.TestCase):
    def test_sibling_prefix_is_not_ancestry_even_for_absolute_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "company"
            sibling = Path(directory) / "company-archive"
            root.mkdir()
            sibling.mkdir()
            target = sibling / "private.txt"
            target.write_text("UNIQUE_SIBLING_CONTENT")
            for variant in ("vulnerable", "fixed"):
                module = load("tenant-storage-prefix", variant)
                for path in ("../company-archive/private.txt", str(target)):
                    with self.subTest(variant=variant, path=path):
                        result = module.read_document(root, path)
                        self.assertEqual(result, {"status": 200, "content": "UNIQUE_SIBLING_CONTENT"} if variant == "vulnerable" else {"status": 403})

    def test_fixed_resolves_symlinks_and_preserves_in_root_normalized_paths(self):
        module = load("tenant-storage-prefix", "fixed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "tenant"
            sibling = Path(directory) / "tenant-backup"
            (root / "docs").mkdir(parents=True)
            sibling.mkdir()
            (root / "report.txt").write_text("OWN_CONTENT")
            (sibling / "private.txt").write_text("FOREIGN_CONTENT")
            (root / "escape").symlink_to(sibling, target_is_directory=True)
            self.assertEqual(module.read_document(root, "escape/private.txt"), {"status": 403})
            self.assertEqual(module.read_document(root, "docs/../report.txt"), {"status": 200, "content": "OWN_CONTENT"})


if __name__ == "__main__":
    unittest.main()
