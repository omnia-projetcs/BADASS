"""Verify the HMAC over the exact request bytes before parsing or updating invoices."""
from contextlib import closing
import hashlib
import hmac
import json
from pathlib import Path
import re
import secrets
import sqlite3


def sign(body, key):
    return "sha256=" + hmac.new(key, body, hashlib.sha256).hexdigest()


def unique_keys(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError("duplicate key")
        result[name] = value
    return result


def handle(body, signature, key, db):
    if not isinstance(body, bytes) or len(body) > 2048:
        return {"status": 400}
    if not isinstance(key, bytes) or len(key) < 32:
        return {"status": 503}
    if not isinstance(signature, str) or not re.fullmatch(r"sha256=[0-9a-f]{64}", signature):
        return {"status": 401}
    # Verify the exact bytes before any parse or business side effect.
    if not hmac.compare_digest(sign(body, key), signature):
        return {"status": 401}
    try:
        event = json.loads(body.decode("utf-8"), object_pairs_hook=unique_keys)
    except (ValueError, UnicodeError, RecursionError):
        return {"status": 400}
    if (not isinstance(event, dict) or set(event) != {"invoice", "amount"}
            or type(event["invoice"]) is not int or not 1 <= event["invoice"] <= 1000
            or type(event["amount"]) is not int or not 1 <= event["amount"] <= 10000):
        return {"status": 400}
    with db:
        invoice = db.execute("SELECT total FROM invoices WHERE id = ?", (event["invoice"],)).fetchone()
        if invoice is None:
            return {"status": 404}
        if invoice[0] != event["amount"]:
            return {"status": 409}
        db.execute("UPDATE invoices SET paid = 1 WHERE id = ?", (event["invoice"],))
    return {"status": 200, "invoice": event["invoice"]}


def run(request):
    # Signing selectors belong to the trusted harness; no signing endpoint is exposed.
    if not isinstance(request, dict) or not isinstance(request.get("body"), str):
        return {"status": 400}
    mode = request.get("signature")
    if mode not in ("valid", "forged", "other-body", "wrong-key", "missing", "malformed"):
        return {"status": 400}
    try:
        body = request["body"].encode("utf-8")
    except UnicodeError:
        return {"status": 400}
    if len(body) > 2048:
        return {"status": 400}
    key = secrets.token_bytes(32)
    signature = sign(body, key)
    if mode == "forged":
        signature = signature[:-1] + ("0" if signature[-1] != "0" else "1")
    elif mode == "other-body":
        signature = sign(b'{"invoice":1,"amount":120}', key)
    elif mode == "wrong-key":
        signature = sign(body, bytes(value ^ 255 for value in key))
    elif mode == "missing":
        signature = None
    elif mode == "malformed":
        signature = "sha256=xyz"
    with closing(sqlite3.connect("invoices.sqlite")) as db:
        db.execute("CREATE TABLE invoices(id INTEGER PRIMARY KEY, total INTEGER, paid INTEGER)")
        db.executemany("INSERT INTO invoices VALUES (?, ?, 0)", [(1, 120), (2, 250)])
        db.commit()
        result = handle(body, signature, key, db)
        state = [list(row) for row in db.execute("SELECT id, total, paid FROM invoices ORDER BY id")]
        Path("invoices-state.json").write_text(json.dumps(state) + "\n", encoding="utf-8")
    return result
