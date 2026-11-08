"""Authorize a model tool call and its destination against server-owned scope."""
from pathlib import Path, PurePosixPath


# This capability was assigned by the operator. Model fields cannot expand it.
CAPABILITIES = {"write_report": frozenset(("reports/findings.txt", "reports/summary.txt"))}


def initialize_workspace():
    # Parents and their lifecycle belong to this local fixture, not the model.
    for name in ("reports", "source"):
        parent = Path(name)
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            return False
        parent.mkdir(exist_ok=True)
    initial = {"reports/findings.txt": "DRAFT_FINDINGS", "reports/summary.txt": "DRAFT_SUMMARY",
               "source/settings.txt": "LAB_SERVER_CONFIG"}
    for name, content in initial.items():
        target = Path(name)
        if target.is_symlink() or (target.exists() and not target.is_file()):
            return False
        if not target.exists():
            target.write_text(content, encoding="utf-8")
    return True


def run(request):
    if not initialize_workspace() or not isinstance(request, dict):
        return {"status": "denied"}
    tool = request.get("tool")
    if not isinstance(tool, str) or tool not in CAPABILITIES:
        return {"status": "denied"}
    arguments = request.get("arguments")
    if not isinstance(arguments, dict):
        return {"status": "denied"}
    name, content = arguments.get("path"), arguments.get("content")
    if not isinstance(name, str) or not name or len(name) > 200:
        return {"status": "denied"}
    if not isinstance(content, str) or len(content) > 2048:
        return {"status": "denied"}
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or len(relative.parts) != 2:
        return {"status": "denied"}
    destination = relative.as_posix()
    if destination not in CAPABILITIES[tool]:
        return {"status": "denied"}
    target = Path(destination)
    if target.parent.is_symlink() or target.is_symlink():
        return {"status": "denied"}
    if target.exists() and not target.is_file():
        return {"status": "denied"}
    target.write_text(content, encoding="utf-8")
    return {"status": "written", "path": destination, "bytes": len(content.encode("utf-8"))}
