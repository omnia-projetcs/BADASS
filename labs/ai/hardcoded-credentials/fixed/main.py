"""AI agent privileged tool guarded by an environment-configured secret."""
import hmac
import os


def _encode_secret(value):
    if not isinstance(value, str) or not value or len(value) > 1024:
        return None
    try:
        return value.encode("utf-8")
    except UnicodeEncodeError:
        return None


def verify_tool_credential(value):
    expected = _encode_secret(os.environ.get("BADASS_ADMIN_PASSWORD"))
    supplied = _encode_secret(value)
    if expected is None or supplied is None:
        return "DENIED"
    return "ADMIN" if hmac.compare_digest(supplied, expected) else "DENIED"


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return verify_tool_credential(tool_call.get("value"))
