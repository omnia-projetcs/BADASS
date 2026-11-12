"""MCP tool registry validating tool names and rejecting directive-injection patterns in metadata."""
import re

APPROVED_TOOLS = {"search_docs", "list_tickets"}
FORBIDDEN_MARKERS = ("IGNORE_POLICY", "EXFILTRATE_SECRET", "SYSTEM:", "<script")


def run(payload):
    if not isinstance(payload, dict):
        return "DENIED"
    tool = payload.get("tool")
    if not isinstance(tool, dict):
        return "DENIED"
    name = tool.get("name")
    description = tool.get("description")
    if name not in APPROVED_TOOLS or not isinstance(description, str):
        return "DENIED"
    if not re.fullmatch(r"[A-Za-z0-9 .,_-]{1,120}", description):
        return "DENIED"
    if any(marker in description.upper() for marker in FORBIDDEN_MARKERS):
        return "DENIED"
    return {"registered": True, "tool": name}
