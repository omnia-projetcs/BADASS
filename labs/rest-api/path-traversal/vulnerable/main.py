"""REST API static document handler vulnerable to relative path traversal."""
from pathlib import Path


def evaluate(value):
    return (Path("public") / value).read_text(encoding="utf-8")


def run(request):
    return evaluate(request["value"])
