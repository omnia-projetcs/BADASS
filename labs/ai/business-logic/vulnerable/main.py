"""AI agent tool for order total calculation without quantity bounds."""


def dispatch_order_tool(value):
    quantity = int(value)
    return str(1000 - quantity * 10)


def run(tool_call):
    # Only the tool argument value is model-supplied; pricing policy is server-side.
    return dispatch_order_tool(tool_call["value"])
