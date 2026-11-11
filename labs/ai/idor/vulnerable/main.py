"""AI agent retrieval tool that fetches any user record without ownership checks."""

AGENT_RECORDS = {"alice": "ALICE_DATA", "bob": "BOB_PRIVATE"}


def dispatch_record_lookup(value):
    return AGENT_RECORDS.get(value, "NOT_FOUND")


def run(tool_call):
    return dispatch_record_lookup(tool_call["value"])
