"""A SQLite sorting expression supplied by a client changes query structure."""
import sqlite3
from contextlib import closing


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("order_by"), str):
        return {"status": 400, "error": "invalid sort"}
    order_by = request["order_by"]
    if not order_by or len(order_by) > 1024:
        return {"status": 400, "error": "invalid sort"}

    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript("""
            CREATE TABLE products(name TEXT NOT NULL, price INTEGER NOT NULL);
            INSERT INTO products VALUES ('alpha', 30), ('beta', 10), ('gamma', 20);
            CREATE TABLE private_config(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            INSERT INTO private_config VALUES ('audit', 'LAB_SECRET');
        """)
        try:
            rows = db.execute("SELECT name FROM products ORDER BY " + order_by + ", name")
            return {"status": 200, "rows": [row[0] for row in rows]}
        except sqlite3.Error:
            return {"status": 400, "error": "invalid sort"}
