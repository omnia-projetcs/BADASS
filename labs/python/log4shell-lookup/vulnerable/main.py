"""Record a log message with an offline expression lookup dependency."""
from pathlib import Path
import re
from urllib.parse import urlsplit

CONFIG = {"LAB_LOG_SECRET": "LAB_PRIVATE_TOKEN"}


def naming_lookup(url):
    return "LAB_LOOKUP_RESULT"


def interpolate(message, calls):
    def lookup(match):
        operation, _, value = match.group(1).partition(":")
        if operation == "env" and value in CONFIG:
            return CONFIG[value]
        if operation == "jndi":
            target = urlsplit(value)
            if target.scheme not in {"ldap", "rmi"} or not target.hostname:
                raise ValueError("unsupported lookup")
            calls.append(value)
            return naming_lookup(value)
        raise ValueError("unsupported lookup")
    for _ in range(8):
        updated, count = re.subn(r"\$\{([^{}]*)\}", lookup, message)
        if not count:
            if "${" in message: raise ValueError("incomplete expression")
            return message
        message = updated
    raise ValueError("too many nested lookups")


def run(request):
    message = request.get("message") if isinstance(request, dict) else None
    if not isinstance(message, str) or len(message) > 1024 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in message):
        return {"status": 400, "error": "invalid message"}
    calls = []
    try:
        rendered = interpolate(message, calls)
        Path("application.log").write_text(rendered + "\n", encoding="utf-8")
        return {"status": 200, "message": rendered, "lookups": calls}
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid message"}
