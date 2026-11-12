"""Agent memory store allowing untrusted retrieved documents to overwrite persistent security policy keys."""


def run(payload):
    memory = {"theme": "light", "security_policy": "strict"}
    for entry in payload.get("entries", []):
        memory[entry["key"]] = entry["value"]
    return memory
