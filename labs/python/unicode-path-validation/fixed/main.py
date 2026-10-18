"""Normalize the filename once, then validate and read its resolved destination."""
from pathlib import Path
import unicodedata


def safe_name(value):
    return (isinstance(value, str) and 1 <= len(value) <= 256
            and ".." not in value and value != "."
            and not any(char in value for char in ("/", "\\", "\x00")))


def read_public(name, root):
    if not isinstance(name, str) or len(name) > 256:
        return {"status": 400}
    name = unicodedata.normalize("NFKC", name)
    if not safe_name(name):
        return {"status": 400}
    try:
        root = Path(root).resolve()
        checked = (root / name).resolve()
        if not checked.is_relative_to(root):
            return {"status": 400}
        # Use the exact resolved path that passed the containment check.
        target = checked
        return {"status": 200, "text": target.read_text(encoding="utf-8")}
    except (OSError, ValueError, UnicodeError):
        return {"status": 404}


def run(name):
    return read_public(name, Path("public"))
