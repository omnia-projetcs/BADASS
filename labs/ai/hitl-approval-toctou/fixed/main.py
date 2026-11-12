"""Human-in-the-loop tool executor binding approval signatures to exact execution parameters."""
import hashlib
import hmac

APPROVAL_KEY = b"LAB_HITL_APPROVAL_KEY"


def sign_action(action_id, recipient, amount):
    msg = f"{action_id}:{recipient}:{amount}".encode("ascii")
    return hmac.new(APPROVAL_KEY, msg, hashlib.sha256).hexdigest()


def run(payload):
    if not isinstance(payload, dict):
        return "DENIED"
    preview = payload.get("preview")
    execution = payload.get("execution")
    if not isinstance(preview, dict) or not isinstance(execution, dict):
        return "DENIED"
    for obj in (preview, execution):
        if not isinstance(obj.get("action_id"), str) or not isinstance(obj.get("recipient"), str):
            return "DENIED"
        if type(obj.get("amount")) is not int or not 1 <= obj["amount"] <= 1000:
            return "DENIED"
    expected_token = sign_action(preview["action_id"], preview["recipient"], preview["amount"])
    exec_token = sign_action(execution["action_id"], execution["recipient"], execution["amount"])
    if not hmac.compare_digest(expected_token, exec_token):
        return "DENIED"
    return {"executed": True, "recipient": execution["recipient"], "amount": execution["amount"]}
