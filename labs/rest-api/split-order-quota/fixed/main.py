"""Batch order endpoint enforcing cumulative account quota across all orders in SQLite."""
from contextlib import closing
import sqlite3

ACCOUNT_QUOTA = 100


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    orders = request.get("orders")
    if not isinstance(orders, list) or not 1 <= len(orders) <= 10:
        return "DENIED"
    for qty in orders:
        if type(qty) is not int or not 1 <= qty <= ACCOUNT_QUOTA:
            return "DENIED"
    with closing(sqlite3.connect("quota.sqlite")) as db:
        db.execute("CREATE TABLE IF NOT EXISTS purchases (account TEXT, qty INTEGER)")
        existing = db.execute("SELECT COALESCE(SUM(qty), 0) FROM purchases WHERE account='alice'").fetchone()[0]
        if existing + sum(orders) > ACCOUNT_QUOTA:
            return "DENIED"
        for qty in orders:
            db.execute("INSERT INTO purchases VALUES ('alice', ?)", (qty,))
        db.commit()
        total = db.execute("SELECT COALESCE(SUM(qty), 0) FROM purchases WHERE account='alice'").fetchone()[0]
    return {"status": 200, "allocated": total}
