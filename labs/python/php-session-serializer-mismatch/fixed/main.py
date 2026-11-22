"""Enforce one structured JSON serializer across upload-progress and session reads."""
import json
from pathlib import Path
import re


KEY_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")


def run(value):
    if not isinstance(value, dict):
        return {"status": 400, "error": "invalid session payload"}
    upload_key = value.get("upload_key")
    note = value.get("note")
    if not isinstance(upload_key, str) or not isinstance(note, str) or not upload_key:
        return {"status": 400, "error": "invalid session payload"}
    if not KEY_RE.fullmatch(upload_key):
        return {"status": 400, "error": "invalid upload key"}

    record = {"upload_" + upload_key: note}
    session_file = Path("session.dat")
    session_file.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    loaded = json.loads(session_file.read_text(encoding="utf-8"))
    return {"status": 200, "values": loaded, "objects": []}
