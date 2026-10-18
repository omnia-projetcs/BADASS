"""Original Host poisoning model inspired by EDB-52485; no email is sent."""
import re
from urllib.parse import urlencode


def reset_url(host, token):
    # Deployment-owned origin; neither Host nor forwarded headers set this value.
    return "https://accounts.example.test/reset-password?" + urlencode({"token": token})


def run(request):
    if not isinstance(request, dict):
        return {"status": 400, "error": "invalid host"}
    host = request.get("host")
    if (not isinstance(host, str) or len(host) > 253
            or not re.fullmatch(r"[A-Za-z0-9.-]+(?::[0-9]{1,5})?", host)):
        return {"status": 400, "error": "invalid host"}
    # This is the captured mail artifact, not a public password-reset response.
    # The fixed marker makes URL expectations deterministic, not a real token.
    return {"recipient": "alice@example.test",
            "reset_url": reset_url(host, "LAB_RESET_TOKEN")}
