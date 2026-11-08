"""Bind setup metadata and process a sequence of synthetic setup requests."""
import os
import re
import sqlite3

PROPERTY = "bootstrapStatusProvider.applicationConfig.setupComplete"


def run(request):
    steps = request.get("steps") if isinstance(request, dict) else None
    if not isinstance(steps, list) or not 1 <= len(steps) <= 6:
        return {"status": 400, "error": "invalid setup request"}
    for item in steps:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or item["path"] not in {"/server-info.action", "/setup/setupadministrator.action"}:
            return {"status": 400, "error": "invalid setup request"}
        params = item.get("params", {})
        if not isinstance(params, dict) or not set(params) <= {PROPERTY} or any(value not in ("true", "false") for value in params.values()):
            return {"status": 400, "error": "invalid setup request"}
        if item["path"] == "/setup/setupadministrator.action" and (not isinstance(item.get("user"), str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,31}", item["user"])):
            return {"status": 400, "error": "invalid setup request"}
    db = sqlite3.connect("setup.sqlite")
    try:
        db.executescript("CREATE TABLE IF NOT EXISTS state(complete INTEGER); CREATE TABLE IF NOT EXISTS users(name TEXT PRIMARY KEY, role TEXT);")
        if db.execute("SELECT COUNT(*) FROM state").fetchone()[0] == 0:
            db.execute("INSERT INTO state VALUES (?)", (0 if os.environ.get("BADASS_SETUP_MODE") == "fresh" else 1,))
            db.commit()
        results = []
        for item in steps:
            params = item.get("params", {})
            if PROPERTY in params:
                db.execute("UPDATE state SET complete = ?", (int(params[PROPERTY] == "true"),))
                db.commit()
            complete = bool(db.execute("SELECT complete FROM state").fetchone()[0])
            if item["path"] == "/server-info.action":
                results.append({"status": 200, "setup_complete": complete})
            elif complete:
                results.append({"status": 403, "error": "setup closed"})
            else:
                db.execute("INSERT OR IGNORE INTO users VALUES (?, 'admin')", (item["user"],))
                db.execute("UPDATE state SET complete = 1")
                db.commit()
                results.append({"status": 201, "created": item["user"]})
        return {"status": 200, "results": results}
    finally:
        db.close()
