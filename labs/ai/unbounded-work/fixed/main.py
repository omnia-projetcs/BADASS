"""AI agent memory buffer tool with strict input and allocation bounds."""


def allocate_agent_buffer(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return "DENIED"
    if isinstance(value, str) and (len(value) > 16 or value.strip().startswith("-0")):
        return "DENIED"
    try:
        size = int(value)
    except ValueError:
        return "DENIED"
    if not 0 <= size <= 100:
        return "DENIED"
    return str(len(bytearray(size)))


def run(tool_call):
    if not isinstance(tool_call, dict) or "value" not in tool_call:
        return "DENIED"
    return allocate_agent_buffer(tool_call["value"])
