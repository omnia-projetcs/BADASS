"""Store a synthetic administrator key after an appliance API check."""
from pathlib import Path
import re


def run(request):
    if not isinstance(request, dict): return {"status": 400, "error": "invalid key request"}
    key, supplied = request.get("key"), request.get("headers", {})
    if not isinstance(key, str) or not re.fullmatch(r"LAB_KEY_[A-Z0-9_]{1,32}", key) or not isinstance(supplied, dict) or len(supplied) > 16:
        return {"status": 400, "error": "invalid key request"}
    headers = {}
    for name, value in supplied.items():
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9-]{1,64}", name) or not isinstance(value, str) or len(value) > 256 or any(ord(c) < 32 or ord(c) == 127 for c in value) or name.lower() in headers:
            return {"status": 400, "error": "invalid key request"}
        headers[name.lower()] = value
    authorized = headers.get("authorization") == "Bearer LAB_ADMIN_API_TOKEN"
    # Forwarding metadata is not an authentication credential.
    if not authorized: return {"status": 401, "error": "denied"}
    Path("appliance-admin.keys").write_text(key + "\n", encoding="utf-8")
    return {"status": 200, "key": key}
