"""Behavioral checks for SQL, HTML, tenant, workflow, and tool-scope extensions."""
from contextlib import contextmanager, closing
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


class InputElements(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


@contextmanager
def fixture(case_id, variant):
    source = ROOT / "labs" / case_id / variant / "main.py"
    spec = importlib.util.spec_from_file_location("extended_fixture", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    previous = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="badass-extension-") as directory:
        try:
            os.chdir(directory)
            yield module, Path(directory)
        finally:
            os.chdir(previous)


class SQLExtensionTests(unittest.TestCase):
    def test_order_by_preserves_each_authorized_sort(self):
        for variant in ("vulnerable", "fixed"):
            for choice, expected in (("name", ["alpha", "beta", "gamma"]),
                                     ("price", ["beta", "gamma", "alpha"])):
                with self.subTest(variant=variant, choice=choice), fixture("python/sql-order-by", variant) as (module, _):
                    self.assertEqual(module.run({"order_by": choice}), {"status": 200, "rows": expected})

    def test_sort_expression_can_observe_private_database_data_only_before_repair(self):
        base = "CASE WHEN (SELECT value FROM private_config WHERE key='audit') = '{}' THEN price ELSE -price END"
        for guess, expected in (("LAB_SECRET", ["beta", "gamma", "alpha"]),
                                ("WRONG", ["alpha", "gamma", "beta"])):
            payload = {"order_by": base.format(guess)}
            with self.subTest(guess=guess), fixture("python/sql-order-by", "vulnerable") as (module, _):
                self.assertEqual(module.run(payload), {"status": 200, "rows": expected})
            with fixture("python/sql-order-by", "fixed") as (module, _):
                self.assertEqual(module.run(payload), {"status": 400, "error": "invalid sort"})

    def test_second_order_storage_preserves_values_without_making_them_trusted(self):
        payloads = (("alice", ["alice"], ["alice"]),
                    ("bob", ["bob"], ["bob"]),
                    ("' OR 1=1 --", ["alice", "bob"], []),
                    ("' UNION SELECT value FROM internal --", ["LAB_SECOND_ORDER_SECRET"], []))
        for name, vulnerable_rows, fixed_rows in payloads:
            for variant, expected in (("vulnerable", vulnerable_rows), ("fixed", fixed_rows)):
                with self.subTest(variant=variant, name=name), fixture("python/sql-second-order", variant) as (module, work):
                    result = module.run({"name": name})
                    self.assertEqual(result, {"status": 200, "stored": name, "matches": expected})
                    # Inspect the real committed database independently of stdout.
                    with closing(sqlite3.connect(work / "saved-search.sqlite")) as db:
                        self.assertEqual(db.execute("SELECT name FROM saved_searches").fetchall(), [(name,)])
                        self.assertEqual(db.execute("SELECT name FROM users ORDER BY name").fetchall(), [("alice",), ("bob",)])

    def test_literal_apostrophe_is_supported_by_the_repaired_second_order_query(self):
        with fixture("python/sql-second-order", "fixed") as (module, _):
            self.assertEqual(module.run({"name": "O'Reilly"}),
                             {"status": 200, "stored": "O'Reilly", "matches": []})


class HTMLAttributeTests(unittest.TestCase):
    def test_repair_preserves_text_in_one_attribute_without_creating_event_handlers(self):
        values = ("Alice & Bob", "O'Reilly", 'Alice "Admin"',
                  '" autofocus onfocus="window.LAB_MARKER=1',
                  'x" onmouseover="window.LAB_MARKER=2')
        for value in values:
            with self.subTest(value=value), fixture("python/xss-attribute", "fixed") as (module, _):
                parser = InputElements()
                parser.feed(module.run({"value": value}))
                self.assertEqual(parser.elements, [("input", {"value": value})])

    def test_vulnerable_body_context_encoder_allows_a_new_html_handler_attribute(self):
        with fixture("python/xss-attribute", "vulnerable") as (module, _):
            parser = InputElements()
            parser.feed(module.run({"value": '" autofocus onfocus="window.LAB_MARKER=1'}))
            self.assertEqual(parser.elements[0][1]["onfocus"], "window.LAB_MARKER=1")


class TenantAuthorizationTests(unittest.TestCase):
    def test_each_server_session_can_access_only_its_tenant(self):
        users = (("LAB_ALICE_SESSION", "invoice-north", "north", "LAB_NORTH_INVOICE", 10),
                 ("LAB_BOB_SESSION", "invoice-south", "south", "LAB_SOUTH_INVOICE", 900))
        for token, invoice_id, tenant_id, memo, total in users:
            for variant in ("vulnerable", "fixed"):
                with self.subTest(token=token, variant=variant), fixture("rest-api/multi-tenant-authorization", variant) as (module, _):
                    self.assertEqual(module.run({"session": token, "invoice_id": invoice_id}),
                                     {"status": 200, "body": {"id": invoice_id, "tenant_id": tenant_id,
                                                               "total": total, "memo": memo}})
        for token, foreign_invoice in (("LAB_ALICE_SESSION", "invoice-south"),
                                       ("LAB_BOB_SESSION", "invoice-north")):
            for variant, expected_status in (("vulnerable", 200), ("fixed", 404)):
                with self.subTest(token=token, variant=variant), fixture("rest-api/multi-tenant-authorization", variant) as (module, _):
                    request = {"session": token, "invoice_id": foreign_invoice,
                               "tenant_id": "south", "role": "admin", "subject": "bob"}
                    self.assertEqual(module.run(request)["status"], expected_status)

    def test_client_identity_fields_do_not_create_an_authenticated_session(self):
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant), fixture("rest-api/multi-tenant-authorization", variant) as (module, _):
                self.assertEqual(module.run({"session": "alice", "subject": "alice", "role": "admin",
                                             "tenant_id": "north", "invoice_id": "invoice-north"}), {"status": 401})


class WorkflowTests(unittest.TestCase):
    def test_paid_order_is_delivered_and_real_ledgers_record_one_effect(self):
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant), fixture("rest-api/order-workflow", variant) as (module, work):
                result = module.run({"actions": ["pay", "deliver"]})
                expected = {"state": "delivered", "charged_cents": 1000, "charges": 1, "shipments": 1}
                self.assertEqual(result["order"], expected)
                self.assertEqual((work / "payments.log").read_text(), "LAB_ORDER_1:1000\n")
                self.assertEqual((work / "shipments.log").read_text(), "LAB_ORDER_1\n")
                self.assertEqual(json.loads((work / "order-state.json").read_text()), expected)

    def test_omitted_payment_and_forged_paid_flag_cannot_create_a_shipment(self):
        for variant, expected_shipments in (("vulnerable", 1), ("fixed", 0)):
            with self.subTest(variant=variant), fixture("rest-api/order-workflow", variant) as (module, work):
                result = module.run({"actions": ["deliver"], "paid": True, "state": "paid", "price": 0})
                self.assertEqual(result["order"]["shipments"], expected_shipments)
                self.assertFalse((work / "payments.log").exists())
                self.assertEqual((work / "shipments.log").exists(), bool(expected_shipments))

    def test_replayed_delivery_has_no_second_shipping_effect_after_repair(self):
        for variant, count in (("vulnerable", 2), ("fixed", 1)):
            with self.subTest(variant=variant), fixture("rest-api/order-workflow", variant) as (module, work):
                result = module.run({"actions": ["pay", "deliver", "deliver"]})
                self.assertEqual(result["order"]["shipments"], count)
                self.assertEqual((work / "shipments.log").read_text().splitlines(), ["LAB_ORDER_1"] * count)
                self.assertEqual((work / "payments.log").read_text().splitlines(), ["LAB_ORDER_1:1000"])


class ToolArgumentScopeTests(unittest.TestCase):
    def test_authorized_destinations_are_written_without_mutating_source(self):
        for variant in ("vulnerable", "fixed"):
            for destination in ("reports/findings.txt", "reports/summary.txt"):
                with self.subTest(variant=variant, destination=destination), fixture("ai/tool-argument-scope", variant) as (module, work):
                    content = "Audit synthetic code: café"
                    result = module.run({"tool": "write_report", "arguments": {"path": destination, "content": content}})
                    self.assertEqual(result, {"status": "written", "path": destination,
                                              "bytes": len(content.encode("utf-8"))})
                    self.assertEqual((work / destination).read_text(), content)
                    self.assertEqual((work / "source/settings.txt").read_text(), "LAB_SERVER_CONFIG")

    def test_model_cannot_expand_a_tool_capability_to_source_files(self):
        for variant, expected in (("vulnerable", "LAB_TAMPERED"), ("fixed", "LAB_SERVER_CONFIG")):
            with self.subTest(variant=variant), fixture("ai/tool-argument-scope", variant) as (module, work):
                module.run({"tool": "write_report", "scope": ["source/settings.txt"], "role": "admin",
                            "arguments": {"path": "source/settings.txt", "content": "LAB_TAMPERED"}})
                self.assertEqual((work / "source/settings.txt").read_text(), expected)

    def test_unissued_report_path_is_not_created(self):
        with fixture("ai/tool-argument-scope", "fixed") as (module, work):
            self.assertEqual(module.run({"tool": "write_report", "arguments": {
                "path": "reports/unapproved.txt", "content": "LAB_TAMPERED"}}), {"status": "denied"})
            self.assertFalse((work / "reports/unapproved.txt").exists())

    def test_traversal_and_a_symlinked_report_parent_are_rejected(self):
        with fixture("ai/tool-argument-scope", "fixed") as (module, work):
            self.assertEqual(module.run({"tool": "write_report", "arguments": {
                "path": "reports/../source/settings.txt", "content": "LAB_TAMPERED"}}), {"status": "denied"})
            self.assertEqual((work / "source/settings.txt").read_text(), "LAB_SERVER_CONFIG")
        with fixture("ai/tool-argument-scope", "fixed") as (module, work):
            (work / "source").mkdir()
            (work / "source/findings.txt").write_text("LAB_SERVER_CONFIG")
            (work / "reports").symlink_to("source", target_is_directory=True)
            self.assertEqual(module.run({"tool": "write_report", "arguments": {
                "path": "reports/findings.txt", "content": "LAB_TAMPERED"}}), {"status": "denied"})
            self.assertEqual((work / "source/findings.txt").read_text(), "LAB_SERVER_CONFIG")


class PrototypeShapeTests(unittest.TestCase):
    def check_node_program(self, source):
        samples = (('{"name":"alice"}', "USER"), ('{"isAdmin":true}', "ADMIN"),
                   ('{"__proto__":{"isAdmin":true}}', "USER"),
                   ('null', "DENIED"), ('[]', "DENIED"), ('true', "DENIED"),
                   ('"text"', "DENIED"), ('42', "DENIED"), ('{', "DENIED"))
        for value, expected in samples:
            with self.subTest(value=value):
                result = subprocess.run(["node", str(source), value], text=True, capture_output=True,
                                        timeout=10, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, "")

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_node_rejects_invalid_shapes_but_preserves_own_properties(self):
        self.check_node_program(ROOT / "labs/node/prototype-pollution/fixed/main.js")

    @unittest.skipUnless(shutil.which("node") and shutil.which("tsc"), "Node.js and TypeScript compiler are required")
    def test_typescript_compiles_strictly_and_enforces_the_same_shape_contract(self):
        with tempfile.TemporaryDirectory(prefix="badass-typescript-") as directory:
            source = ROOT / "labs/typescript/prototype-pollution/fixed/main.ts"
            result = subprocess.run(["tsc", "--strict", "--target", "ES2020", "--module", "commonjs",
                                     "--outDir", directory, str(source)], text=True, capture_output=True,
                                    timeout=30, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.check_node_program(Path(directory) / "main.js")


if __name__ == "__main__":
    unittest.main()
