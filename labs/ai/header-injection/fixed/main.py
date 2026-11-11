"""AI agent webhook formatter that rejects CR/LF and control characters."""


def format_agent_header(value):
    if not isinstance(value, str) or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return "DENIED"
    return "X-User: " + value + "\r\n\r\nBODY"


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return format_agent_header(tool_call.get("value"))
