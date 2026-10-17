"""An untrusted search survives safe storage, then becomes SQL in a later phase."""
import sqlite3
from contextlib import closing


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("name"), str):
        return {"status": 400, "error": "invalid name"}
    if len(request["name"]) > 1024:
        return {"status": 400, "error": "invalid name"}

    # The owned, temporary fixture directory holds this synthetic database.
    with closing(sqlite3.connect("saved-search.sqlite")) as db:
        db.executescript("""
            CREATE TABLE saved_searches(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE users(name TEXT NOT NULL);
            INSERT INTO users VALUES ('alice'), ('bob');
            CREATE TABLE internal(value TEXT NOT NULL);
            INSERT INTO internal VALUES ('LAB_SECOND_ORDER_SECRET');
        """)
        db.execute("INSERT INTO saved_searches(id, name) VALUES (1, ?)", (request["name"],))
        db.commit()

    # A separate connection represents a later report using the stored value.
    with closing(sqlite3.connect("saved-search.sqlite")) as db:
        stored = db.execute("SELECT name FROM saved_searches WHERE id = 1").fetchone()[0]
        try:
            rows = db.execute("SELECT name FROM users WHERE name = '" + stored + "'")
            return {"status": 200, "stored": stored, "matches": [row[0] for row in rows]}
        except sqlite3.Error:
            return {"status": 400, "error": "invalid saved query"}
