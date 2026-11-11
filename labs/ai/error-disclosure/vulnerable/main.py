"""AI agent tool that leaks internal connection secrets in exception responses."""
from pathlib import Path


def dispatch_status_tool(value):
    if value == "ok":
        return "OK"
    try:
        Path("missing-database").read_text(encoding="utf-8")
    except FileNotFoundError:
        return "db://admin:LAB_SECRET@database/internal"
    return "OK"


def run(tool_call):
    return dispatch_status_tool(tool_call["value"])
