"""Original upload validation model inspired by EDB-45169; files are never run."""
from pathlib import Path
import re


def run(request):
    if not isinstance(request, dict):
        return {"status": 400, "error": "invalid upload"}
    name, content, mime = (request.get(k) for k in ("filename", "content", "content_type"))
    if (not isinstance(name, str) or len(name) > 100
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name)
            or not isinstance(content, str) or len(content) > 4096 or "\x00" in content
            or not isinstance(mime, str)):
        return {"status": 400, "error": "invalid upload"}
    try:
        content.encode("utf-8")
    except UnicodeEncodeError:
        return {"status": 400, "error": "invalid upload"}
    # This service accepts plain text and CSV attachments only.
    allowed = {".txt": "text/plain", ".csv": "text/csv"}
    if Path(name).suffix.lower() not in allowed or allowed[Path(name).suffix.lower()] != mime:
        return {"status": 415, "error": "unsupported upload type"}
    root = Path("uploads")
    root.mkdir(exist_ok=True)
    target = root / name
    # Exclusive creation avoids symlink following and silent overwrites.
    try:
        with target.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except FileExistsError:
        return {"status": 409, "error": "file already exists"}
    return {"status": 201, "path": target.as_posix()}
