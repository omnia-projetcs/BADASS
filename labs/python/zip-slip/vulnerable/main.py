"""Intentional ZIP extraction traversal; inspired by EDB-39816."""
from io import BytesIO
from pathlib import Path
import zipfile


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("members"), list):
        return {"status": 400, "error": "invalid archive"}
    members = request["members"]
    if not 1 <= len(members) <= 16 or any(
        not isinstance(m, dict)
        or not isinstance(m.get("name"), str) or not 1 <= len(m["name"]) <= 256
        or "\x00" in m["name"] or m["name"].endswith(("/", "\\"))
        or not isinstance(m.get("content"), str) or len(m["content"]) > 4096
        for m in members
    ):
        return {"status": 400, "error": "invalid archive"}
    # Build an actual ZIP from JSON-friendly, bounded synthetic members.
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for member in members:
            archive.writestr(member["name"], member["content"])
    root = Path("uploads").resolve()
    root.mkdir(exist_ok=True)
    with zipfile.ZipFile(buffer) as archive:
        for member in archive.infolist():
            # VULNERABLE: joining a path does not confine it to the extraction root.
            target = root / member.filename.replace("\\", "/")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    return {"status": 200, "extracted": len(members)}
