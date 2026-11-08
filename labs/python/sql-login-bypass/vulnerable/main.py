"""Intentional SQL login bypass; original teaching fixture inspired by EDB-41029."""
from contextlib import closing
import hashlib
import sqlite3


def password_key(password):
    # Fixed salt and known passwords belong only to this disposable fixture.
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"BADASS-login-demo", 100_000).hex()


def run(request):
    if not isinstance(request, dict) or any(
        not isinstance(request.get(key), str) or not 1 <= len(request[key]) <= 256
        or "\x00" in request[key] for key in ("username", "password")
    ):
        return {"status": 400, "error": "invalid credentials"}
    with closing(sqlite3.connect(":memory:")) as db:
        db.execute("CREATE TABLE users(username TEXT PRIMARY KEY, password_key TEXT, role TEXT)")
        db.executemany("INSERT INTO users VALUES (?, ?, ?)", [
            ("admin", password_key("LAB_ADMIN_PASSWORD"), "admin"),
            ("alice", password_key("LAB_ALICE_PASSWORD"), "reader"),
            ("O'Reilly", password_key("LAB_READER_PASSWORD"), "reader"),
        ])
        key = password_key(request["password"])
        # VULNERABLE: username changes SQL structure, including the password predicate.
        query = "SELECT username, role FROM users WHERE username = '" + request["username"] + "' AND password_key = '" + key + "'"
        try:
            user = db.execute(query).fetchone()
        except sqlite3.Error:
            return {"status": 400, "error": "invalid query"}
        if user is None:
            return {"status": 401, "error": "denied"}
        return {"status": 200, "user": user[0], "role": user[1]}
