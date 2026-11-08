"""A first-key-wins gateway forwards raw JSON to a last-key-wins worker."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3


def first_wins(pairs):
    result = {}
    for key, value in pairs:
        result.setdefault(key, value)
    return result


def valid_payment(value, limit):
    return (isinstance(value, dict) and set(value) == {"amount", "recipient"}
            and type(value["amount"]) is int and 1 <= value["amount"] <= limit
            and value["recipient"] == "vendor")


def transfer(raw, db):
    if not isinstance(raw, str) or len(raw) > 1024:
        return {"status": 400}
    try:
        checked = json.loads(raw, object_pairs_hook=first_wins)
        if not valid_payment(checked, 100):
            return {"status": 400}
        # The worker receives the original bytes, not the validated values.
        payment = json.loads(raw)
        if not valid_payment(payment, 5000):
            return {"status": 400}
    except (ValueError, RecursionError):
        return {"status": 400}
    with db:
        changed = db.execute("UPDATE wallet SET balance = balance - ? WHERE id = 1 AND balance >= ?",
                             (payment["amount"], payment["amount"]))
        if changed.rowcount != 1:
            return {"status": 409}
        db.execute("INSERT INTO payments(amount, recipient) VALUES (?, ?)",
                   (payment["amount"], payment["recipient"]))
    return {"status": 201, "amount": payment["amount"]}


def run(raw):
    with closing(sqlite3.connect("payments.sqlite")) as db:
        db.execute("CREATE TABLE wallet(id INTEGER PRIMARY KEY, balance INTEGER)")
        db.execute("INSERT INTO wallet VALUES (1, 5000)")
        db.execute("CREATE TABLE payments(amount INTEGER, recipient TEXT)")
        db.commit()
        result = transfer(raw, db)
        snapshot = {"balance": db.execute("SELECT balance FROM wallet").fetchone()[0],
                    "payments": [list(row) for row in db.execute("SELECT amount, recipient FROM payments")]}
        Path("payments-state.json").write_text(json.dumps(snapshot, sort_keys=True) + "\n", encoding="utf-8")
    return result
