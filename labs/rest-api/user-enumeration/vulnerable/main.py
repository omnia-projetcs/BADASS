"""Login endpoint returning distinct error messages and skipping hash work for unknown accounts."""
import hashlib

USERS = {"alice": hashlib.pbkdf2_hmac("sha256", b"correct-horse", b"fixed-salt-alice", 1000).hex()}


def run(request):
    user = request.get("user", "")
    password = request.get("password", "")
    if user not in USERS:
        return {"status": 404, "error": "USER_NOT_FOUND"}
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), b"fixed-salt-alice", 1000).hex()
    if digest != USERS[user]:
        return {"status": 401, "error": "WRONG_PASSWORD"}
    return {"status": 200, "user": user}
