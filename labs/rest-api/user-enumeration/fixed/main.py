"""Login endpoint enforcing uniform error responses and constant-work password verification."""
import hashlib
import hmac

USERS = {"alice": hashlib.pbkdf2_hmac("sha256", b"correct-horse", b"fixed-salt-alice", 1000).hex()}
DUMMY_DIGEST = hashlib.pbkdf2_hmac("sha256", b"dummy-password", b"fixed-salt-dummy", 1000).hex()


def run(request):
    if not isinstance(request, dict):
        return {"status": 401, "error": "INVALID_CREDENTIALS"}
    user = request.get("user")
    password = request.get("password")
    if not isinstance(user, str) or not isinstance(password, str):
        return {"status": 401, "error": "INVALID_CREDENTIALS"}
    expected = USERS.get(user, DUMMY_DIGEST)
    salt = b"fixed-salt-alice" if user in USERS else b"fixed-salt-dummy"
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 1000).hex()
    if hmac.compare_digest(candidate, expected) and user in USERS:
        return {"status": 200, "user": user}
    return {"status": 401, "error": "INVALID_CREDENTIALS"}
