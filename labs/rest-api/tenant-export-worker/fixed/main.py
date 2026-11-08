"""Preserve the trusted tenant scope through the queue and worker SQL query."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3


SESSIONS = {"LAB_NORTH_SESSION": "north", "LAB_SOUTH_SESSION": "south"}
DOCUMENTS = [("north", 1, "LAB_NORTH_EXPORT"), ("south", 1, "LAB_SOUTH_EXPORT"),
             ("south", 2, "LAB_SOUTH_SECOND_EXPORT")]


def execute_job(job, database):
    # This separate connection models a worker with no ambient HTTP session.
    with closing(sqlite3.connect(database)) as db:
        # Retain the trusted tenant from the queued job at the data sink.
        row = db.execute("SELECT content FROM documents WHERE tenant = ? AND id = ?",
                         (job["tenant"], job["document_id"])).fetchone()
    if row is None:
        return {"status": 404}
    Path("export.txt").write_text(row[0], encoding="utf-8")
    return {"status": 200, "content": row[0]}


def run(request):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    identifier = request.get("document_id")
    if type(identifier) is not int or not 1 <= identifier <= 1000:
        return {"status": 400}
    tenant = SESSIONS[token]
    database = "exports.sqlite"
    with closing(sqlite3.connect(database)) as db:
        db.execute("CREATE TABLE documents(tenant TEXT, id INTEGER, content TEXT, PRIMARY KEY(tenant,id))")
        db.executemany("INSERT INTO documents VALUES (?, ?, ?)", DOCUMENTS)
        db.commit()
        if db.execute("SELECT 1 FROM documents WHERE tenant = ? AND id = ?", (tenant, identifier)).fetchone() is None:
            return {"status": 404}
    # Enqueue trusted scope, persist it, and reload it as a worker would.
    job = {"tenant": tenant, "document_id": identifier}
    Path("queued-job.json").write_text(json.dumps(job, sort_keys=True) + "\n", encoding="utf-8")
    return execute_job(json.loads(Path("queued-job.json").read_text()), database)
