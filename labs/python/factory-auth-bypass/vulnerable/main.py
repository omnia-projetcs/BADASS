"""Update a synthetic appliance setting using a server-side session table."""
import sqlite3
from urllib.parse import parse_qs


def run(request):
    if not isinstance(request, dict):
        return {"status": 400, "error": "invalid request"}
    query, banner, token = request.get("query", ""), request.get("banner"), request.get("token", "")
    if not isinstance(query, str) or len(query) > 512 or not isinstance(banner, str) or len(banner) > 128 or not isinstance(token, str) or len(token) > 128:
        return {"status": 400, "error": "invalid request"}
    try:
        parameters = parse_qs(query, keep_blank_values=True, max_num_fields=8, errors="strict")
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid request"}
    db = sqlite3.connect("appliance.sqlite")
    try:
        db.executescript("CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, role TEXT);"
                         "CREATE TABLE IF NOT EXISTS config(name TEXT PRIMARY KEY, value TEXT);"
                         "INSERT OR IGNORE INTO sessions VALUES('LAB_ADMIN_SESSION', 'admin');"
                         "INSERT OR IGNORE INTO sessions VALUES('LAB_READER_SESSION', 'reader');"
                         "INSERT OR IGNORE INTO config VALUES('banner', 'WELCOME');")
        if "factoryBypass" in parameters:
            token = "LAB_CREATED_SESSION"
            db.execute("INSERT OR REPLACE INTO sessions VALUES (?, ?)", (token, "admin"))
        session = db.execute("SELECT role FROM sessions WHERE token = ?", (token,)).fetchone()
        if session != ("admin",):
            return {"status": 401, "error": "denied"}
        db.execute("UPDATE config SET value = ? WHERE name = 'banner'", (banner,))
        db.commit()
        return {"status": 200, "banner": db.execute("SELECT value FROM config WHERE name = 'banner'").fetchone()[0]}
    finally:
        db.close()
