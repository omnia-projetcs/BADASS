"""A string-prefix check mistakes a sibling tenant directory for a child path."""
from pathlib import Path


SESSIONS = {"LAB_NORTH_SESSION": "north", "LAB_BACKUP_SESSION": "north-backup", "LAB_SOUTH_SESSION": "south"}
FILES = {"north/report.txt": "LAB_NORTH_STORAGE",
         "north/docs/notes.txt": "LAB_NORTH_NOTES",
         "north-backup/private.txt": "LAB_BACKUP_PRIVATE",
         "south/private.txt": "LAB_SOUTH_PRIVATE"}


def read_document(root, name):
    if not isinstance(name, str) or not 1 <= len(name) <= 256 or "\x00" in name:
        return {"status": 400}
    try:
        root = root.resolve()
        target = (root / name).resolve()
        # VULNERABLE: /north-backup has prefix /north but is not within /north.
        if not str(target).startswith(str(root)):
            return {"status": 403}
        if not target.is_file():
            return {"status": 404}
        return {"status": 200, "content": target.read_text(encoding="utf-8")}
    except (OSError, ValueError, RuntimeError, UnicodeError):
        return {"status": 400}


def run(request):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    # The fixture owns its directory tree; request fields cannot pick its root.
    storage = Path("storage")
    for relative, content in FILES.items():
        path = storage / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return read_document(storage / SESSIONS[token], request.get("path"))
