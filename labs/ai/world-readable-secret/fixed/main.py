"""AI agent credential store that sets descriptor permissions before closing."""
from pathlib import Path
import os


def store_agent_artifact(value):
    if not isinstance(value, str):
        return "DENIED"
    mode = 0o644 if value == "public" else 0o600
    fd = os.open("stored-secret", os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        os.fchmod(stream.fileno(), mode)
        stream.write("PUBLIC" if value == "public" else "LAB_SECRET")
    return format(Path("stored-secret").stat().st_mode & 0o777, "04o")


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return store_agent_artifact(tool_call.get("value"))
