"""AI agent policy guard that fails closed on backend errors or invalid tokens."""
import hmac


def verify_agent_policy(value):
    if not isinstance(value, str) or not value.isascii():
        return "DENIED"
    try:
        if value == "backend-down":
            raise ConnectionError("Policy backend unavailable")
        return "ALLOWED" if hmac.compare_digest(value, "authorized") else "DENIED"
    except ConnectionError:
        return "DENIED"


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return verify_agent_policy(tool_call.get("value"))
