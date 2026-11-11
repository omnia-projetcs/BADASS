"""AI agent credential store that resets secret file permissions to world-readable."""
from pathlib import Path
import os


def store_agent_artifact(value):
    fd = os.open("stored-secret", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write("PUBLIC" if value == "public" else "LAB_SECRET")
    os.chmod("stored-secret", 0o644)
    return format(Path("stored-secret").stat().st_mode & 0o777, "04o")


def run(tool_call):
    return store_agent_artifact(tool_call["value"])
