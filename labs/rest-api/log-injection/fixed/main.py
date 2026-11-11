"""REST API audit logger that escapes CR, LF, and backslashes in log lines."""
from pathlib import Path


def evaluate(value):
    if not isinstance(value, str):
        return "DENIED"
    value = value.replace("\\", "\\\\").replace("\r", r"\r").replace("\n", r"\n")
    record = "user=" + value
    Path("audit.log").write_text(record, encoding="utf-8")
    return Path("audit.log").read_bytes().decode("utf-8")


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
