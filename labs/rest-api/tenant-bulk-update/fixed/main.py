"""Authorize every document before applying an atomic tenant-scoped batch."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3


SESSIONS = {"LAB_NORTH_SESSION": "north", "LAB_SOUTH_SESSION": "south"}
DOCUMENTS = [(1, "north", 0), (2, "north", 0), (3, "south", 0), (4, "south", 0)]


def archive(request, db):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    ids = request.get("document_ids")
    if (not isinstance(ids, list) or not 1 <= len(ids) <= 8
            or any(type(i) is not int or not 1 <= i <= 1000 for i in ids)
            or len(set(ids)) != len(ids)):
        return {"status": 400}
    tenant = SESSIONS[token]
    with db:
        db.execute("BEGIN IMMEDIATE")
        owners = [db.execute("SELECT tenant FROM documents WHERE id = ?", (i,)).fetchone() for i in ids]
        if any(owner is None for owner in owners):
            return {"status": 404}
        # Validate every object before any write in the same transaction.
        if any(owner[0] != tenant for owner in owners):
            return {"status": 403}
        db.executemany("UPDATE documents SET archived = 1 WHERE id = ? AND tenant = ?", [(i, tenant) for i in ids])
    return {"status": 200, "archived": ids}


def run(request):
    with closing(sqlite3.connect("documents.sqlite")) as db:
        db.execute("CREATE TABLE documents(id INTEGER PRIMARY KEY, tenant TEXT, archived INTEGER)")
        db.executemany("INSERT INTO documents VALUES (?, ?, ?)", DOCUMENTS)
        db.commit()
        result = archive(request, db)
        state = [{"id": i, "tenant": tenant, "archived": bool(archived)}
                 for i, tenant, archived in db.execute("SELECT id, tenant, archived FROM documents ORDER BY id")]
        Path("documents-state.json").write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")
    return result
