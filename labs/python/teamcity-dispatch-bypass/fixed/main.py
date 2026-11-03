"""Dispatch a synthetic admin request after optional JSP forwarding."""
import sqlite3
from urllib.parse import parse_qs

SESSIONS = {"LAB_ADMIN_SESSION": "admin", "LAB_READER_SESSION": "reader"}
PRIVATE = "/app/rest/users"


def run(request):
    if not isinstance(request, dict):
        return {"status": 400, "error": "invalid request"}
    path, query, token = request.get("path"), request.get("query", ""), request.get("token", "")
    if not all(isinstance(value, str) and len(value) <= 512 and not any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in value) for value in (path, query, token)):
        return {"status": 400, "error": "invalid request"}
    try:
        parameters = parse_qs(query, keep_blank_values=True, max_num_fields=8, errors="strict")
        targets = parameters.get("jsp", [])
        if len(targets) > 1 or (targets and not targets[0].endswith(".jsp")):
            raise ValueError("invalid forward")
        effective = targets[0].split(";", 1)[0] if targets else path
        if effective not in {PRIVATE, "/login.html", "/health"}:
            return {"status": 404, "error": "missing route"}
        if effective == PRIVATE and SESSIONS.get(token) != "admin":
            return {"status": 401, "error": "denied"}
        if effective == "/login.html": return {"status": 200, "page": "login"}
        if effective == "/health": return {"status": 200, "health": "ok"}
        db = sqlite3.connect("teamcity.sqlite")
        try:
            db.execute("CREATE TABLE IF NOT EXISTS users(name TEXT PRIMARY KEY, role TEXT)")
            db.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ("lab-user", "admin"))
            db.commit()
            return {"status": 201, "created": "lab-user"}
        finally:
            db.close()
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid request"}
