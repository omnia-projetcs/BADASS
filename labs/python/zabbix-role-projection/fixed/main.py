"""Retrieve the authenticated user's role using a dynamic SQL projection."""
import sqlite3


def run(request):
    if not isinstance(request, dict) or request.get("token") != "LAB_API_READER":
        return {"status": 401, "error": "denied"}
    fields = request.get("selectRole")
    if not isinstance(fields, list) or not 1 <= len(fields) <= 4 or any(not isinstance(field, str) or not field or len(field) > 256 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in field) for field in fields):
        return {"status": 400, "error": "invalid projection"}
    allowed = {"name": "name", "roleid": "roleid"}
    if any(field not in allowed for field in fields):
        return {"status": 400, "error": "invalid projection"}
    fields = [allowed[field] for field in fields]
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    try:
        db.executescript("CREATE TABLE roles(roleid INTEGER, name TEXT, token TEXT);"
                         "INSERT INTO roles VALUES(1, 'reader', 'LAB_READER_TOKEN'), (9, 'admin', 'LAB_ADMIN_TOKEN');")
        row = db.execute("SELECT " + ",".join(fields) + " FROM roles WHERE roleid = ?", (1,)).fetchone()
        return {"status": 200, "role": dict(row)}
    except sqlite3.Error:
        return {"status": 400, "error": "invalid projection"}
    finally:
        db.close()
