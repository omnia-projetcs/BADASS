"""MCP tool registry concatenating untrusted tool descriptions directly into agent system instructions."""


def run(payload):
    tool = payload.get("tool", {})
    description = tool.get("description", "")
    if "EXFILTRATE_SECRET" in description or "IGNORE_POLICY" in description:
        return {"registered": True, "effect": "POLICY_OVERRIDDEN"}
    return {"registered": True, "tool": tool.get("name", "")}
