"""A filename is validated before compatibility normalization changes its path."""
from pathlib import Path
import unicodedata


def safe_name(value):
    return (isinstance(value, str) and 1 <= len(value) <= 256
            and ".." not in value and value != "."
            and not any(char in value for char in ("/", "\\", "\x00")))


def read_public(name, root):
    if not safe_name(name):
        return {"status": 400}
    try:
        root = Path(root).resolve()
        checked = (root / name).resolve()
        if not checked.is_relative_to(root):
            return {"status": 400}
        # Downstream normalization invalidates the checks on the original name.
        target = root / unicodedata.normalize("NFKC", name)
        return {"status": 200, "text": target.read_text(encoding="utf-8")}
    except (OSError, ValueError, UnicodeError):
        return {"status": 404}


def run(name):
    return read_public(name, Path("public"))
