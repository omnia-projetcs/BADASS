"""AI agent scratch writer that follows pre-placed symlinks in the workspace."""
from pathlib import Path


def write_agent_scratch(value):
    if value == "preplaced-link":
        Path("export.tmp").symlink_to("secret.txt")
    try:
        with open("export.tmp", "w", encoding="utf-8") as stream:
            stream.write("LAB_OVERWRITTEN")
    except FileExistsError:
        pass
    return Path("secret.txt").read_text(encoding="utf-8")


def run(tool_call):
    return write_agent_scratch(tool_call["value"])
