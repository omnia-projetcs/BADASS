"""Real password recovery updates with an expiring but reusable reset token."""
from contextlib import closing
import hashlib
import hmac
import secrets
import sqlite3


NOW = 1000
INITIAL_PASSWORD = "Initial-LAB-password"


def digest(password, salt):
    # Local benchmark cost; production password policy and tuning are out of scope.
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200000)


def initialize(db):
    db.execute("CREATE TABLE accounts(id INTEGER PRIMARY KEY, salt BLOB, password_hash BLOB)")
    db.execute("CREATE TABLE reset_tokens(token_hash TEXT PRIMARY KEY, account_id INTEGER, expires INTEGER, used INTEGER)")
    salt = secrets.token_bytes(16)
    db.execute("INSERT INTO accounts VALUES (1, ?, ?)", (salt, digest(INITIAL_PASSWORD, salt)))
    token = secrets.token_urlsafe(32)
    db.execute("INSERT INTO reset_tokens VALUES (?, 1, ?, 0)",
               (hashlib.sha256(token.encode()).hexdigest(), NOW + 100))
    db.commit()
    return token


def password_matches(db, password):
    salt, expected = db.execute("SELECT salt, password_hash FROM accounts WHERE id = 1").fetchone()
    return hmac.compare_digest(digest(password, salt), expected)


def valid_password(password):
    if not isinstance(password, str) or not 8 <= len(password) <= 128:
        return False
    try:
        password.encode("utf-8")
    except UnicodeError:
        return False
    return True


def reset_password(db, token, password, now):
    if (not isinstance(token, str) or not token.isascii() or not 1 <= len(token) <= 128
            or not valid_password(password) or type(now) is not int):
        return {"status": 400}
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    with db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT account_id FROM reset_tokens WHERE token_hash = ? AND expires > ? AND used = 0",
                         (token_hash, now)).fetchone()
        if row is None:
            return {"status": 403}
        # Missing consumption: the same credential remains eligible until expiry.
        salt = secrets.token_bytes(16)
        db.execute("UPDATE accounts SET salt = ?, password_hash = ? WHERE id = ?",
                   (salt, digest(password, salt), row[0]))
    return {"status": 200}


def run(request):
    # Attempts and timestamps are harness controls, not a production API contract.
    if not isinstance(request, dict) or not isinstance(request.get("attempts"), list):
        return {"status": 400}
    attempts = request["attempts"]
    if not 1 <= len(attempts) <= 4:
        return {"status": 400}
    for attempt in attempts:
        if (not isinstance(attempt, dict) or attempt.get("token") not in ("issued", "unknown")
                or not valid_password(attempt.get("password"))
                or type(attempt.get("at")) is not int or not NOW <= attempt["at"] <= NOW + 1000):
            return {"status": 400}
    with closing(sqlite3.connect("recovery.sqlite")) as db:
        token = initialize(db)
        statuses = [reset_password(db, token if a["token"] == "issued" else "UNKNOWN_LAB_TOKEN",
                                   a["password"], a["at"])["status"] for a in attempts]
        # Trusted observation of actual credential verification, not an API response.
        return {"statuses": statuses,
                "password_matches": [password_matches(db, a["password"]) for a in attempts],
                "initial_password_works": password_matches(db, INITIAL_PASSWORD)}
