"""AI agent memory buffer tool without allocation limits."""


def allocate_agent_buffer(value):
    size = int(value)
    return str(len(bytearray(size)))


def run(tool_call):
    return allocate_agent_buffer(tool_call["value"])
