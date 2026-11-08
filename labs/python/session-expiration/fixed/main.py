"""Reject expired or revoked sessions before accessing account data."""
from contextlib import closing
import hashlib
import secrets
import sqlite3


NOW = 1000


def initialize(db):
    db.execute("CREATE TABLE sessions(token_hash TEXT PRIMARY KEY, owner TEXT, expires INTEGER, revoked INTEGER)")
    db.execute("CREATE TABLE reports(owner TEXT PRIMARY KEY, body TEXT)")
    token = secrets.token_urlsafe(32)
    db.execute("INSERT INTO sessions VALUES (?, 'alice', ?, 0)",
               (hashlib.sha256(token.encode()).hexdigest(), NOW + 60))
    db.execute("INSERT INTO reports VALUES ('alice', 'LAB_PRIVATE_REPORT')")
    db.commit()
    return token


def dispatch(db, token, operation, now):
    if (not isinstance(token, str) or not token.isascii() or not 1 <= len(token) <= 128
            or operation not in ("read", "logout") or type(now) is not int):
        return {"status": 400}
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    session = db.execute("SELECT owner, expires, revoked FROM sessions WHERE token_hash = ?", (token_hash,)).fetchone()
    if session is None:
        return {"status": 401}
    # A persisted row is not sufficient: both lifecycle checks must still pass.
    if session[1] <= now or session[2]:
        return {"status": 401}
    if operation == "logout":
        with db:
            db.execute("UPDATE sessions SET revoked = 1 WHERE token_hash = ?", (token_hash,))
        return {"status": 204}
    report = db.execute("SELECT body FROM reports WHERE owner = ?", (session[0],)).fetchone()
    return {"status": 200, "report": report[0]} if report else {"status": 404}


def run(request):
    # Clock values and token selectors are controlled by the scenario harness.
    if not isinstance(request, dict) or not isinstance(request.get("actions"), list):
        return {"status": 400}
    actions = request["actions"]
    if not 1 <= len(actions) <= 4:
        return {"status": 400}
    previous = NOW
    for action in actions:
        if (not isinstance(action, dict) or action.get("op") not in ("read", "logout")
                or action.get("token") not in ("issued", "unknown")
                or type(action.get("at")) is not int or not previous <= action["at"] <= NOW + 3600):
            return {"status": 400}
        previous = action["at"]
    with closing(sqlite3.connect("sessions.sqlite")) as db:
        token = initialize(db)
        return {"events": [dispatch(db, token if a["token"] == "issued" else "UNKNOWN_LAB_TOKEN", a["op"], a["at"])
                           for a in actions]}
