"""Model upload-progress serializer mismatch allowing delimiter-injected objects."""
from pathlib import Path
import re


OBJECT_RE = re.compile(r'O:\d+:"([A-Za-z0-9_]+)":\d+:\{[^}]*\}')
PAIR_RE = re.compile(r'^a:1:\{s:\d+:"([^"]*)";s:\d+:"([^"]*)";\}$')


def write_upload_progress(upload_key, note):
    # Written with php_serialize-style framing (no '|' escaping).
    key_str = "upload_" + upload_key
    data = f'a:1:{{s:{len(key_str)}:"{key_str}";s:{len(note)}:"{note}";}}'
    Path("session.dat").write_text(data, encoding="utf-8")


def read_php_session():
    # Read back with php's '|' key/value delimiter serializer.
    raw = Path("session.dat").read_text(encoding="utf-8")
    objects = []
    values = {}
    if "|" in raw:
        _, rest = raw.split("|", 1)
        obj = OBJECT_RE.match(rest)
        if obj:
            cls = obj.group(1)
            objects.append(cls)
            Path("deserialized-object.txt").write_text(cls + "\n", encoding="utf-8")
            return values, objects
    pair = PAIR_RE.match(raw)
    if pair:
        values[pair.group(1)] = pair.group(2)
    return values, objects


def run(value):
    if not isinstance(value, dict):
        return {"status": 400, "error": "invalid session payload"}
    upload_key = value.get("upload_key")
    note = value.get("note")
    if not isinstance(upload_key, str) or not isinstance(note, str) or not upload_key:
        return {"status": 400, "error": "invalid session payload"}
    write_upload_progress(upload_key, note)
    values, objects = read_php_session()
    return {"status": 200, "values": values, "objects": objects}
