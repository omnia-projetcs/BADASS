"""Record a log message without evaluating message-embedded lookup expressions."""
from pathlib import Path

CONFIG = {"LAB_LOG_SECRET": "LAB_PRIVATE_TOKEN"}


def naming_lookup(url):
    raise RuntimeError("Naming lookup is disabled")


def run(request):
    message = request.get("message") if isinstance(request, dict) else None
    if not isinstance(message, str) or len(message) > 1024 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in message):
        return {"status": 400, "error": "invalid message"}
    calls = []
    try:
        rendered = message
        Path("application.log").write_text(rendered + "\n", encoding="utf-8")
        return {"status": 200, "message": rendered, "lookups": calls}
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid message"}
