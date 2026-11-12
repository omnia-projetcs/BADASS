"""Document store login handler enforcing scalar string types and constant-time key comparison."""
import hmac

DOCUMENTS = [
    {"user": "alice", "api_key": "LAB_ALICE_KEY", "role": "admin"},
    {"user": "bob", "api_key": "LAB_BOB_KEY", "role": "viewer"},
]


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    user = request.get("user")
    api_key = request.get("api_key")
    if not isinstance(user, str) or not isinstance(api_key, str):
        return "DENIED"
    if not user.isascii() or not api_key.isascii():
        return "DENIED"
    for doc in DOCUMENTS:
        if doc["user"] == user and hmac.compare_digest(doc["api_key"], api_key):
            return {"authenticated": doc["user"], "role": doc["role"]}
    return "DENIED"
