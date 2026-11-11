"""REST API audit logger that writes unescaped user strings into log lines."""
from pathlib import Path


def evaluate(value):
    record = "user=" + value
    Path("audit.log").write_text(record, encoding="utf-8")
    return Path("audit.log").read_bytes().decode("utf-8")


def run(request):
    return evaluate(request["value"])
