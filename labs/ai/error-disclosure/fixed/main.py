"""AI agent tool that redacts internal connection strings on storage errors."""
from pathlib import Path


def dispatch_status_tool(value):
    if value == "ok":
        return "OK"
    try:
        Path("missing-database").read_text(encoding="utf-8")
    except FileNotFoundError:
        return "Service unavailable"
    return "OK"


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "Service unavailable"
    return dispatch_status_tool(tool_call.get("value"))
