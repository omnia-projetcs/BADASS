"""AI agent telemetry logger that writes raw model strings into audit logs."""
from pathlib import Path


def record_agent_event(value):
    entry = "user=" + value
    Path("audit.log").write_text(entry, encoding="utf-8")
    return Path("audit.log").read_bytes().decode("utf-8")


def run(tool_call):
    return record_agent_event(tool_call["value"])
