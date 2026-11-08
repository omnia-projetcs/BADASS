"""Observe tenant separation at cache, role, queue and SQLite mutation boundaries."""
from contextlib import contextmanager, closing
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(slug, variant):
    spec = importlib.util.spec_from_file_location("tenant_fixture", ROOT / f"labs/rest-api/{slug}/{variant}/main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invoke(work, slug, variant, request):
    result = subprocess.run([sys.executable, str(ROOT / "tools/invoke.py"),
                             str(ROOT / f"labs/rest-api/{slug}/{variant}/main.py"), json.dumps(request)],
                            cwd=work, capture_output=True, text=True, timeout=10, check=True)
    return json.loads(result.stdout)


@contextmanager
def workspace():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as directory:
        try:
            os.chdir(directory)
            yield Path(directory)
        finally:
            os.chdir(previous)


class CacheIsolationTests(unittest.TestCase):
    def test_tenant_order_does_not_change_fixed_visibility(self):
        for variant in ("vulnerable", "fixed"):
            for order in (("north", "south"), ("south", "north")):
                with self.subTest(variant=variant, order=order):
                    module = load("tenant-cache", variant)
                    cache = {}
                    for tenant in order:
                        response = module.fetch({"session": f"LAB_{tenant.upper()}_SESSION", "document_id": "summary"}, cache)
                        expected_tenant = tenant if variant == "fixed" else order[0]
                        self.assertEqual(response["content"], f"LAB_{expected_tenant.upper()}_PRIVATE_SUMMARY")
                    self.assertEqual(len(cache), 2 if variant == "fixed" else 1)

    def test_fixed_cache_cannot_supply_a_document_absent_from_requester_tenant(self):
        module = load("tenant-cache", "fixed")
        module.DOCUMENTS[("north", "private-only")] = "NORTH_ONLY"
        cache = {}
        self.assertEqual(module.fetch({"session": "LAB_NORTH_SESSION", "document_id": "private-only"}, cache)["status"], 200)
        self.assertEqual(module.fetch({"session": "LAB_SOUTH_SESSION", "document_id": "private-only"}, cache), {"status": 404})
        self.assertEqual(module.fetch({"session": "INVALID", "document_id": "private-only"}, cache), {"status": 401})

    def test_fixed_key_handles_additional_tenants_without_literal_special_cases(self):
        module = load("tenant-cache", "fixed")
        module.SESSIONS["LAB_THIRD_SESSION"] = "third"
        module.DOCUMENTS[("third", "summary")] = "THIRD_PRIVATE"
        cache = {}
        module.fetch({"session": "LAB_NORTH_SESSION", "document_id": "summary"}, cache)
        self.assertEqual(module.fetch({"session": "LAB_THIRD_SESSION", "document_id": "summary", "tenant_id": "north"}, cache),
                         {"status": 200, "content": "THIRD_PRIVATE"})


class ScopedRoleTests(unittest.TestCase):
    def test_current_target_membership_controls_mutation(self):
        module = load("tenant-admin-scope", "fixed")
        accounts = deepcopy(module.ACCOUNTS)
        request = {"session": "LAB_NORTH_ADMIN", "account_id": "south-member", "tenant_id": "north", "role": "admin"}
        self.assertEqual(module.disable(request, accounts), {"status": 403})
        self.assertEqual(accounts, module.ACCOUNTS)
        module.SESSIONS["LAB_NORTH_ADMIN"]["south"] = "admin"
        self.assertEqual(module.disable(request, accounts), {"status": 200, "disabled": "south-member"})
        self.assertTrue(accounts["north-member"]["active"])
        self.assertFalse(accounts["south-member"]["active"])

    def test_denied_cross_tenant_mutation_preserves_persisted_accounts(self):
        with workspace() as work:
            result = invoke(work, "tenant-admin-scope", "fixed",
                            {"session": "LAB_SOUTH_ADMIN", "account_id": "north-member"})
            self.assertEqual(result, {"status": 403})
            state = json.loads((work / "accounts-state.json").read_text())
            self.assertTrue(all(account["active"] for account in state.values()))


class ExportWorkerTests(unittest.TestCase):
    def test_queue_uses_authenticated_tenant_and_worker_exports_that_tenant(self):
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant), workspace() as work:
                response = invoke(work, "tenant-export-worker", variant,
                                  {"session": "LAB_SOUTH_SESSION", "document_id": 1, "tenant": "north"})
                self.assertEqual(json.loads((work / "queued-job.json").read_text()), {"tenant": "south", "document_id": 1})
                with closing(sqlite3.connect(work / "exports.sqlite")) as db:
                    expected_tenant = "south" if variant == "fixed" else "north"
                    expected = db.execute("SELECT content FROM documents WHERE tenant=? AND id=1", (expected_tenant,)).fetchone()[0]
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM documents WHERE id=1").fetchone()[0], 2)
                self.assertEqual((work / "export.txt").read_text(), expected)
                self.assertEqual(response, {"status": 200, "content": expected})

    def test_fixed_worker_scopes_arbitrary_trusted_job_tenants(self):
        module = load("tenant-export-worker", "fixed")
        with workspace() as work:
            database = work / "custom.sqlite"
            with closing(sqlite3.connect(database)) as db:
                db.execute("CREATE TABLE documents(tenant TEXT, id INTEGER, content TEXT)")
                db.executemany("INSERT INTO documents VALUES (?, ?, ?)", [("east", 42, "EAST_ONLY"), ("west", 42, "WEST_ONLY")])
                db.commit()
            for tenant in ("east", "west"):
                self.assertEqual(module.execute_job({"tenant": tenant, "document_id": 42}, database),
                                 {"status": 200, "content": tenant.upper() + "_ONLY"})
            (work / "export.txt").unlink()
            self.assertEqual(module.execute_job({"tenant": "east' OR 1=1 --", "document_id": 42}, database), {"status": 404})
            self.assertFalse((work / "export.txt").exists())


class BulkIsolationTests(unittest.TestCase):
    def test_mixed_batch_rejection_is_atomic_and_vulnerable_effect_is_real(self):
        for variant in ("vulnerable", "fixed"):
            for session, ids in (("LAB_NORTH_SESSION", [1, 3]), ("LAB_SOUTH_SESSION", [3, 1])):
                with self.subTest(variant=variant, ids=ids), workspace() as work:
                    response = invoke(work, "tenant-bulk-update", variant, {"session": session, "document_ids": ids})
                    self.assertEqual(response["status"], 200 if variant == "vulnerable" else 403)
                    with closing(sqlite3.connect(work / "documents.sqlite")) as db:
                        changed = [row[0] for row in db.execute("SELECT id FROM documents WHERE archived = 1 ORDER BY id")]
                    self.assertEqual(changed, sorted(ids) if variant == "vulnerable" else [])

    def test_rejected_batch_does_not_prevent_a_later_authorized_batch(self):
        module = load("tenant-bulk-update", "fixed")
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("CREATE TABLE documents(id INTEGER PRIMARY KEY, tenant TEXT, archived INTEGER)")
            db.executemany("INSERT INTO documents VALUES (?, ?, ?)", module.DOCUMENTS)
            db.commit()
            for ids in ([1, 3], [3, 1], [1, 99]):
                self.assertIn(module.archive({"session": "LAB_NORTH_SESSION", "document_ids": ids}, db)["status"], (403, 404))
                self.assertEqual(db.execute("SELECT SUM(archived) FROM documents").fetchone()[0], 0)
            self.assertEqual(module.archive({"session": "LAB_NORTH_SESSION", "document_ids": [1, 2]}, db)["status"], 200)
            self.assertEqual(db.execute("SELECT id, archived FROM documents ORDER BY id").fetchall(), [(1, 1), (2, 1), (3, 0), (4, 0)])


if __name__ == "__main__":
    unittest.main()
