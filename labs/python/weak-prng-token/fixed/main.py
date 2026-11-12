"""Session token issuer using CSPRNG secrets and rejecting deterministic Mersenne Twister tokens."""
import hmac
import secrets


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    if request.get("mode") == "health":
        return "OK"
    token = request.get("token")
    if not isinstance(token, str) or len(token) != 64:
        return "DENIED"
    admin_token = secrets.token_hex(32)
    return "ADMIN_SESSION" if hmac.compare_digest(token, admin_token) else "DENIED"
