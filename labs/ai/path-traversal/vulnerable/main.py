"""AI agent file reader tool that joins model paths without confinement."""
from pathlib import Path


def read_agent_document(value):
    return (Path("public") / value).read_text(encoding="utf-8")


def run(tool_call):
    return read_agent_document(tool_call["value"])
