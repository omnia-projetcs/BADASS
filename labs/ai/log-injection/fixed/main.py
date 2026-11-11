"""AI agent telemetry logger that escapes line breaks before writing audit logs."""
from pathlib import Path


def record_agent_event(value):
    if not isinstance(value, str):
        return "DENIED"
    escaped = value.replace("\\", "\\\\").replace("\r", r"\r").replace("\n", r"\n")
    entry = "user=" + escaped
    Path("audit.log").write_text(entry, encoding="utf-8")
    return Path("audit.log").read_bytes().decode("utf-8")


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return record_agent_event(tool_call.get("value"))
