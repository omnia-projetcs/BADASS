"""Download a local text file after URL path processing."""
from pathlib import Path
from urllib.parse import unquote


def run(value):
    if not isinstance(value, str) or not value or len(value) > 512 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in value):
        return {"status": 400, "error": "invalid path"}
    root = Path("public").resolve()
    try:
        first = unquote(value, errors="strict")
        if "\x00" in first:
            return {"status": 400, "error": "invalid path"}
        if ".." in first.split("/") or first.startswith("/"):
            return {"status": 403, "error": "outside public root"}
        target = root / unquote(first, errors="strict")
        if target.is_file():
            return {"status": 200, "body": target.read_text(encoding="utf-8")}
        return {"status": 404, "error": "missing file"}
    except (OSError, ValueError, UnicodeError, RuntimeError):
        return {"status": 400, "error": "invalid path"}
