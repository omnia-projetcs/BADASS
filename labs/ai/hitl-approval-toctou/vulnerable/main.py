"""Human-in-the-loop tool executor checking only the approval ID while allowing argument mutation."""
import hashlib
import hmac

APPROVAL_KEY = b"LAB_HITL_APPROVAL_KEY"


def sign_preview(action_id, recipient, amount):
    msg = f"{action_id}:{recipient}:{amount}".encode("ascii")
    return hmac.new(APPROVAL_KEY, msg, hashlib.sha256).hexdigest()


def run(payload):
    preview = payload["preview"]
    execution = payload["execution"]
    # Vulnerable: verifies that a preview existed for action_id, ignoring mutated recipient/amount.
    if preview.get("action_id") != execution.get("action_id"):
        return "DENIED"
    return {"executed": True, "recipient": execution["recipient"], "amount": execution["amount"]}
