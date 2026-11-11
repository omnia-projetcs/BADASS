"""AI agent retrieval tool that enforces the caller's server-owned principal."""

AGENT_RECORDS = {"alice": "ALICE_DATA", "bob": "BOB_PRIVATE"}
CALLER_PRINCIPAL = "alice"


def dispatch_record_lookup(value):
    if not isinstance(value, str):
        return "DENIED"
    if value in AGENT_RECORDS and value != CALLER_PRINCIPAL:
        return "DENIED"
    return AGENT_RECORDS.get(value, "NOT_FOUND")


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return dispatch_record_lookup(tool_call.get("value"))
