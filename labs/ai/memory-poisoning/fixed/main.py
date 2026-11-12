"""Agent memory store restricting untrusted writes to user-preference keys with provenance checks."""

USER_MUTABLE_KEYS = {"theme", "locale"}
ALLOWED_VALUES = {"theme": {"light", "dark"}, "locale": {"en", "fr"}}


def run(payload):
    if not isinstance(payload, dict):
        return "DENIED"
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        return "DENIED"
    memory = {"theme": "light", "security_policy": "strict"}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("source") != "trusted_user":
            return "DENIED"
        key = entry.get("key")
        val = entry.get("value")
        if key not in USER_MUTABLE_KEYS or val not in ALLOWED_VALUES[key]:
            return "DENIED"
        memory[key] = val
    return memory
