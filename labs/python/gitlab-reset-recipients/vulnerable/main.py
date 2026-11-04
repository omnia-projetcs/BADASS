"""Queue synthetic password reset deliveries after resolving an account."""
import json
from pathlib import Path
import re

VERIFIED = {"alice": {"alice@example.test", "alice.alt@example.test"}, "bob": {"bob@example.test"}}


def run(request):
    supplied = request.get("email") if isinstance(request, dict) else None
    recipients = [supplied] if isinstance(supplied, str) else supplied
    if not isinstance(recipients, list) or not 1 <= len(recipients) <= 4 or any(not isinstance(item, str) or len(item) > 128 or not re.fullmatch(r"[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+", item) for item in recipients):
        return {"status": 400, "error": "invalid recovery request"}
    recipients = list(dict.fromkeys(item.lower() for item in recipients))
    accounts = [name for name, addresses in VERIFIED.items() if set(recipients) & addresses]
    if len(accounts) > 1: return {"status": 400, "error": "invalid recovery request"}
    if not accounts: return {"status": 202, "queued": 0}
    account = accounts[0]
    pass
    outbox = [{"to": item, "token": "LAB_RESET_TOKEN"} for item in recipients]
    Path("outbox.json").write_text(json.dumps(outbox, sort_keys=True) + "\n", encoding="utf-8")
    return {"status": 202, "queued": len(outbox)}
