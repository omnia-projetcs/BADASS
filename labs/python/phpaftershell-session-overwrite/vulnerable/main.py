"""Model non-atomic in-place session overwrite leaving hybrid serialized bytes."""
from pathlib import Path
import re


OBJECT_RE = re.compile(r'O:\d+:"([A-Za-z0-9_]+)":\d+:\{[^}]*\}')
STRING_RE = re.compile(r's:(\d+):"([^"]*)"')


def parse_session(raw):
    values = {}
    objects = []
    pos = 0
    while pos < len(raw):
        sep = raw.find("|", pos)
        if sep == -1:
            break
        key = raw[pos:sep]
        rest = raw[sep + 1:]
        obj = OBJECT_RE.match(rest)
        if obj:
            cls = obj.group(1)
            objects.append(cls)
            Path("gadget-ran.txt").write_text(cls + "\n", encoding="utf-8")
            pos = sep + 1 + obj.end()
            if pos < len(raw) and raw[pos] == ";":
                pos += 1
            continue
        str_match = STRING_RE.match(rest)
        if str_match:
            values[key] = str_match.group(2)
            pos = sep + 1 + str_match.end()
            if pos < len(raw) and raw[pos] == ";":
                pos += 1
            continue
        break
    return values, objects


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

    # Overwrite in place without truncating first; an interruption leaves old trailing bytes.
    payload = update.encode("utf-8")
    with session_file.open("r+b") as handle:
        if interrupt_at is not None and interrupt_at < len(payload):
            handle.write(payload[:interrupt_at])
        else:
            handle.write(payload)
            handle.truncate(len(payload))

    raw = session_file.read_text(encoding="utf-8", errors="replace")
    values, objects = parse_session(raw)
    return {"status": 200, "values": values, "objects": objects}
