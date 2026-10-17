"""Inspect committed shipment rows and real worker activity independently."""
from contextlib import closing
import importlib.util
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def load_fixture(variant):
    source = ROOT / "labs/rest-api/order-concurrency" / variant / "main.py"
    spec = importlib.util.spec_from_file_location("concurrency_fixture", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OrderConcurrencyTests(unittest.TestCase):
    def exercise(self, variant, count, expected_shipments):
        module = load_fixture(variant)
        previous = Path.cwd()
        with tempfile.TemporaryDirectory(prefix="badass-order-concurrency-") as directory:
            work = Path(directory)
            try:
                os.chdir(work)
                original_connect = sqlite3.connect
                main_thread = threading.get_ident()
                worker_threads = set()
                observation_lock = threading.Lock()

                def observe(statement):
                    if threading.get_ident() != main_thread:
                        with observation_lock:
                            worker_threads.add(threading.get_ident())

                def traced_connection(*args, **kwargs):
                    connection = original_connect(*args, **kwargs)
                    connection.set_trace_callback(observe)
                    return connection

                with patch.object(module.sqlite3, "connect", side_effect=traced_connection):
                    result = module.run({"requests": count, "state": "untrusted-client-state"})

                # Successful output alone is insufficient: both workers must
                # execute SQL, and committed state plus the effect log must agree.
                self.assertEqual(len(worker_threads), count)
                with closing(original_connect(work / "order-concurrency.sqlite")) as db:
                    self.assertEqual(db.execute("SELECT state FROM orders WHERE id = 1").fetchone(), ("delivered",))
                    self.assertEqual(db.execute("SELECT order_id FROM shipments ORDER BY id").fetchall(),
                                     [(1,)] * expected_shipments)
                    self.assertEqual(db.execute("PRAGMA integrity_check").fetchone(), ("ok",))
                self.assertEqual((work / "shipments.log").read_text().splitlines(),
                                 ["LAB_ORDER_1"] * expected_shipments)
                self.assertEqual(result, {"status": 200, "requests": count, "accepted": expected_shipments,
                                          "rejected": count - expected_shipments,
                                          "state": "delivered", "shipments": expected_shipments})
            finally:
                os.chdir(previous)

    def test_one_authorized_request_delivers_once_in_both_variants(self):
        for variant in ("vulnerable", "fixed"):
            with self.subTest(variant=variant):
                self.exercise(variant, 1, 1)

    def test_simultaneous_requests_only_duplicate_delivery_before_repair(self):
        for variant, expected in (("vulnerable", 2), ("fixed", 1)):
            with self.subTest(variant=variant):
                self.exercise(variant, 2, expected)

    def test_invalid_request_counts_create_no_database_or_shipment_log(self):
        previous = Path.cwd()
        for variant in ("vulnerable", "fixed"):
            module = load_fixture(variant)
            for count in (0, 3, True, "2", None):
                with self.subTest(variant=variant, count=count), tempfile.TemporaryDirectory(prefix="badass-order-invalid-") as directory:
                    try:
                        os.chdir(directory)
                        self.assertEqual(module.run({"requests": count}),
                                         {"status": 400, "error": "requests must be 1 or 2"})
                        self.assertFalse(Path("order-concurrency.sqlite").exists())
                        self.assertFalse(Path("shipments.log").exists())
                    finally:
                        os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
