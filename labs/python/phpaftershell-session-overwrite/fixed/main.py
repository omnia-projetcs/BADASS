"""Write session updates atomically and reject serialized object tags."""
import os
from pathlib import Path
import re


STRING_RE = re.compile(r's:(\d+):"([^"]*)"')


def parse_session_safe(raw):
    values = {}
    pos = 0
    while pos < len(raw):
        sep = raw.find("|", pos)
        if sep == -1:
            return None
        key = raw[pos:sep]
        if not key or not re.fullmatch(r"[A-Za-z0-9_.-]+", key):
            return None
        rest = raw[sep + 1:]
        str_match = STRING_RE.match(rest)
        if not str_match:
            return None
        declared_len = int(str_match.group(1))
        text = str_match.group(2)
        if len(text.encode("utf-8")) != declared_len:
            return None
        values[key] = text
        pos = sep + 1 + str_match.end()
        if pos < len(raw) and raw[pos] == ";":
            pos += 1
    return values


def run(value):
    if not isinstance(value, dict):
        return {"status": 400, "error": "invalid session operation"}
    initial = value.get("initial")
    update = value.get("update")
    interrupt_at = value.get("interrupt_at")
    if not isinstance(initial, str) or not isinstance(update, str):
        return {"status": 400, "error": "invalid session operation"}
    if interrupt_at is not None and (type(interrupt_at) is not int or interrupt_at < 0):
        return {"status": 400, "error": "invalid session operation"}

    session_file = Path("session.dat")
    session_file.write_bytes(initial.encode("utf-8"))

    payload = update.encode("utf-8")
    tmp_file = Path("session.dat.tmp")
    if interrupt_at is not None and interrupt_at < len(payload):
        # Abort partial write cleanly without touching the committed session file.
        tmp_file.write_bytes(payload[:interrupt_at])
        tmp_file.unlink(missing_ok=True)
        return {"status": 409, "error": "interrupted session write"}

    tmp_file.write_bytes(payload)
    os.replace(tmp_file, session_file)

    raw = session_file.read_text(encoding="utf-8", errors="strict")
    values = parse_session_safe(raw)
    if values is None:
        return {"status": 400, "error": "corrupted session data"}
    return {"status": 200, "values": values, "objects": []}
