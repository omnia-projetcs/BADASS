"""REST API secret writer that sets permissions on the open file descriptor."""
from pathlib import Path
import os


def evaluate(value):
    if not isinstance(value, str):
        return "DENIED"
    mode = 0o644 if value == "public" else 0o600
    fd = os.open("stored-secret", os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        os.fchmod(stream.fileno(), mode)
        stream.write("PUBLIC" if value == "public" else "LAB_SECRET")
    return format(Path("stored-secret").stat().st_mode & 0o777, "04o")


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
