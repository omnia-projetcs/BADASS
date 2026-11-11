"""REST API static document handler restricted to allowlisted filenames."""
from pathlib import Path


def evaluate(value):
    if not isinstance(value, str) or value != "welcome.txt":
        return "DENIED"
    return (Path("public") / value).read_text(encoding="utf-8")


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
