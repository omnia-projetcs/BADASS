"""Agent tool router that restricts execution to operator-approved read-only tools."""

ALLOWED_TOOLS = frozenset({"read_source", "report_finding"})


def run(call):
    if not isinstance(call, dict):
        return "DENIED"
    tool = call.get("tool")
    if not isinstance(tool, str) or tool not in ALLOWED_TOOLS:
        return "DENIED"
    return "EXECUTED:" + tool
