"""AI agent tool for order total calculation with strict quantity bounds."""


def dispatch_order_tool(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return "DENIED"
    if isinstance(value, str) and (len(value) > 16 or value.strip().startswith("-0")):
        return "DENIED"
    try:
        quantity = int(value)
    except ValueError:
        return "DENIED"
    if not 1 <= quantity <= 100:
        return "DENIED"
    return str(1000 - quantity * 10)


def run(tool_call):
    if not isinstance(tool_call, dict) or "value" not in tool_call:
        return "DENIED"
    return dispatch_order_tool(tool_call["value"])
