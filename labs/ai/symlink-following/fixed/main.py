"""AI agent scratch writer that refuses to overwrite existing files or symlinks."""
from pathlib import Path


def write_agent_scratch(value):
    if not isinstance(value, str):
        return "DENIED"
    if value == "preplaced-link":
        Path("export.tmp").symlink_to("secret.txt")
    try:
        with open("export.tmp", "x", encoding="utf-8") as stream:
            stream.write("LAB_OVERWRITTEN")
    except FileExistsError:
        pass
    return Path("secret.txt").read_text(encoding="utf-8")


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return write_agent_scratch(tool_call.get("value"))
