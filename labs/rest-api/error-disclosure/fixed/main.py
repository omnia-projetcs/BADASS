"""REST API handler that returns a generic error message when storage fails."""
from pathlib import Path


def evaluate(value):
    if value == "ok":
        return "OK"
    try:
        Path("missing-database").read_text(encoding="utf-8")
    except FileNotFoundError:
        return "Service unavailable"
    return "OK"


def run(request):
    if not isinstance(request, dict):
        return "Service unavailable"
    return evaluate(request.get("value"))
