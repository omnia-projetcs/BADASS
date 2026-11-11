"""AI agent file reader tool restricted to allowlisted public documents."""
from pathlib import Path

ALLOWED_DOCUMENTS = frozenset({"welcome.txt"})


def read_agent_document(value):
    if not isinstance(value, str) or value not in ALLOWED_DOCUMENTS:
        return "DENIED"
    root = Path("public").resolve()
    target = (root / value).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        return "DENIED"
    return target.read_text(encoding="utf-8")


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return read_agent_document(tool_call.get("value"))
