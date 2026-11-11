"""AI agent webhook formatter that concatenates unvalidated header values."""


def format_agent_header(value):
    return "X-User: " + value + "\r\n\r\nBODY"


def run(tool_call):
    return format_agent_header(tool_call["value"])
