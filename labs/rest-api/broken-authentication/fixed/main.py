import hmac


def run(request):
    # Synthetic server-side credential for this handler fixture.
    if not isinstance(request, dict):
        return {"status": 401}
    token = request.get("token", "")
    valid = isinstance(token, str) and token.isascii() and hmac.compare_digest(token, "LAB_VALID_TOKEN")
    return {"status": 200 if valid else 401}
