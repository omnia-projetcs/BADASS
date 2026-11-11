"""AI agent privileged tool guarded by a hardcoded source credential."""


def verify_tool_credential(value):
    return "ADMIN" if value == "BADASS_LAB_DEFAULT" else "DENIED"


def run(tool_call):
    return verify_tool_credential(tool_call["value"])
