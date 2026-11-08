"""Download a local text file after URL path processing."""
from pathlib import Path
from urllib.parse import unquote


def run(value):
    if not isinstance(value, str) or not value or len(value) > 512 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in value):
        return {"status": 400, "error": "invalid path"}
    root = Path("public").resolve()
    try:
        decoded = value
        for _ in range(4):
            next_value = unquote(decoded, errors="strict")
            if next_value == decoded:
                break
            decoded = next_value
        if "%" in decoded or "\\" in decoded or "\x00" in decoded:
            return {"status": 400, "error": "invalid path"}
        target = (root / decoded).resolve()
        if not target.is_relative_to(root):
            return {"status": 403, "error": "outside public root"}
        if target.is_file():
            return {"status": 200, "body": target.read_text(encoding="utf-8")}
        return {"status": 404, "error": "missing file"}
    except (OSError, ValueError, UnicodeError, RuntimeError):
        return {"status": 400, "error": "invalid path"}
