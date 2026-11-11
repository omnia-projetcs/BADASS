"""REST API secret writer that leaves stored secret files world-readable."""
from pathlib import Path
import os


def evaluate(value):
    fd = os.open("stored-secret", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write("PUBLIC" if value == "public" else "LAB_SECRET")
    os.chmod("stored-secret", 0o644)
    return format(Path("stored-secret").stat().st_mode & 0o777, "04o")


def run(request):
    return evaluate(request["value"])
