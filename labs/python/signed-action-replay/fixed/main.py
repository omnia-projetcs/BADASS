"""Reject reused signed action identifiers before applying a second debit."""
import hashlib
import hmac
import json
from pathlib import Path
import re
import secrets


NOW = 1000


def sign(body, key):
    return hmac.new(key, body, hashlib.sha256).hexdigest()


class Processor:
    def __init__(self, key, balance=1000):
        self.key = key
        self.balance = balance
        self.seen = set()
        self.accepted = []

    def process(self, body, tag, now):
        if (not isinstance(body, bytes) or len(body) > 512 or not isinstance(tag, str)
                or not re.fullmatch(r"[0-9a-f]{64}", tag)
                or not hmac.compare_digest(sign(body, self.key), tag)):
            return {"status": 401}
        try:
            event = json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeError, RecursionError):
            return {"status": 400}
        if (not isinstance(event, dict) or set(event) != {"id", "amount", "expires"}
                or not isinstance(event["id"], str) or not re.fullmatch(r"[a-z0-9-]{1,32}", event["id"])
                or type(event["amount"]) not in (int, float) or not 1 <= event["amount"] <= 500 or event["amount"] % 1 != 0
                or type(event["expires"]) not in (int, float) or not NOW <= event["expires"] <= 2000 or event["expires"] % 1 != 0):
            return {"status": 400}
        if event["expires"] <= now:
            return {"status": 401}
        # Replay state belongs to this sequential processor instance.
        if event["id"] in self.seen:
            return {"status": 409}
        if event["amount"] > self.balance:
            return {"status": 402}
        self.seen.add(event["id"])
        self.balance -= int(event["amount"])
        self.accepted.append({"id": event["id"], "amount": int(event["amount"])})
        return {"status": 200}


def run(request):
    # Signed actions and clock values are local scenario controls.
    if not isinstance(request, dict) or not isinstance(request.get("actions"), list):
        return {"status": 400}
    actions = request["actions"]
    if not 1 <= len(actions) <= 6:
        return {"status": 400}
    previous = NOW
    for action in actions:
        if (not isinstance(action, dict) or action.get("signature") not in ("valid", "forged")
                or type(action.get("at")) not in (int, float)
                or not previous <= action["at"] <= 2000 or action["at"] % 1 != 0):
            return {"status": 400}
        previous = action["at"]
    key = secrets.token_bytes(32)
    processor = Processor(key)
    statuses = []
    for action in actions:
        body = json.dumps({"id": action.get("id"), "amount": action.get("amount"), "expires": NOW + 60}, separators=(",", ":")).encode()
        tag = sign(body, key)
        if action["signature"] == "forged":
            tag = ("0" if tag[0] != "0" else "1") + tag[1:]
        statuses.append(processor.process(body, tag, action["at"])["status"])
    state = {"balance": processor.balance, "accepted": processor.accepted}
    Path("ledger.json").write_text(json.dumps(state, separators=(",", ":")) + "\n", encoding="utf-8")
    return {"statuses": statuses, "balance": processor.balance}
