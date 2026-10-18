"""Confined ZIP extraction counterpart; inspired by EDB-39816."""
from io import BytesIO
from pathlib import Path, PureWindowsPath
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
        targets = []
        # Validate every member before writing any member of a rejected archive.
        for member in archive.infolist():
            name = member.filename.replace("\\", "/")
            relative = Path(name)
            target = (root / relative).resolve()
            if (relative.is_absolute() or PureWindowsPath(name).drive
                    or ".." in relative.parts or not target.is_relative_to(root)
                    or target == root or target in [path for _, path in targets]):
                return {"status": 400, "error": "unsafe archive path"}
            targets.append((member, target))
        # The fixture directory is owned by this process; no concurrent writers.
        for member, target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    return {"status": 200, "extracted": len(members)}
