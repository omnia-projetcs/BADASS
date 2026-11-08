import hmac


def run(request):
    # The fixture stands in for an authenticated server-side session token.
    expected = "lab-session-csrf-token"
    if not isinstance(request, dict):
        return "DENIED"
    token = request.get("csrf", "")
    if not isinstance(token, str) or not token.isascii() or not hmac.compare_digest(token, expected):
        return "DENIED"
    return "TRANSFERRED"
