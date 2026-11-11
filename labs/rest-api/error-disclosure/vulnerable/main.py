"""REST API handler that returns internal connection credentials when storage fails."""
from pathlib import Path


def evaluate(value):
    if value == "ok":
        return "OK"
    try:
        Path("missing-database").read_text(encoding="utf-8")
    except FileNotFoundError:
        return "db://admin:LAB_SECRET@database/internal"
    return "OK"


def run(request):
    return evaluate(request["value"])
