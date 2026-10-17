"""An atomic local SQLite transition gives one request the right to ship.

This fixture exercises real concurrent transactions on one SQLite database.
The log records local synthetic effects; crash-safe delivery to external systems
would require an outbox or another durable dispatch protocol.
"""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
import sqlite3
import threading


def run(request):
    if not isinstance(request, dict) or type(request.get("requests")) is not int:
        return {"status": 400, "error": "requests must be 1 or 2"}
    count = request["requests"]
    if count not in (1, 2):
        return {"status": 400, "error": "requests must be 1 or 2"}

    database = "order-concurrency.sqlite"
    # A paid order is established by the server, not by client-supplied flags.
    with closing(sqlite3.connect(database)) as db:
        db.executescript("""
            CREATE TABLE orders(id INTEGER PRIMARY KEY, state TEXT NOT NULL);
            INSERT INTO orders VALUES (1, 'paid');
            CREATE TABLE shipments(id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL);
        """)
        db.commit()

    gate = threading.Barrier(count, timeout=5)
    log_lock = threading.Lock()

    def deliver():
        with closing(sqlite3.connect(database, timeout=5, isolation_level=None)) as db:
            # No thread holds a write lock while waiting for its peer.
            gate.wait()
            try:
                db.execute("BEGIN IMMEDIATE")
                changed = db.execute("UPDATE orders SET state = 'delivered' "
                                     "WHERE id = 1 AND state = 'paid'").rowcount
                if changed == 1:
                    db.execute("INSERT INTO shipments(order_id) VALUES (1)")
                db.commit()
            except Exception:
                db.rollback()
                raise
            if changed != 1:
                return False
            with log_lock:
                with Path("shipments.log").open("a", encoding="utf-8") as ledger:
                    ledger.write("LAB_ORDER_1\n")
            return True

    with ThreadPoolExecutor(max_workers=count) as workers:
        futures = [workers.submit(deliver) for _ in range(count)]
        accepted = sum(future.result(timeout=12) for future in futures)

    with closing(sqlite3.connect(database)) as db:
        state = db.execute("SELECT state FROM orders WHERE id = 1").fetchone()[0]
        shipments = db.execute("SELECT COUNT(*) FROM shipments WHERE order_id = 1").fetchone()[0]
    return {"status": 200, "requests": count, "accepted": accepted,
            "rejected": count - accepted, "state": state, "shipments": shipments}
