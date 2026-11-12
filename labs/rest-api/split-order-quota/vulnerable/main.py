"""Batch order endpoint enforcing per-item limit without checking cumulative account quota."""
from contextlib import closing
import sqlite3


def run(request):
    orders = request.get("orders", [])
    with closing(sqlite3.connect("quota.sqlite")) as db:
        db.execute("CREATE TABLE IF NOT EXISTS purchases (account TEXT, qty INTEGER)")
        for qty in orders:
            if type(qty) is not int or not 1 <= qty <= 100:
                return "DENIED"
            db.execute("INSERT INTO purchases VALUES ('alice', ?)", (qty,))
        db.commit()
        total = db.execute("SELECT COALESCE(SUM(qty), 0) FROM purchases WHERE account='alice'").fetchone()[0]
    return {"status": 200, "allocated": total}
