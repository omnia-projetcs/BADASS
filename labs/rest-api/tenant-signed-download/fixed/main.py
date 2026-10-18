"""Corrected tenant-signed-download fixture with explicit tenant boundaries."""
import hashlib
import hmac
import json
import re
import secrets


NOW = 2_000_000_000  # Pinned laboratory clock.
SESSIONS = {"LAB_NORTH_SESSION": "north", "LAB_SOUTH_SESSION": "south"}
DOCUMENTS = {("north", "report"): "LAB_NORTH_SHARED_REPORT",
             ("south", "report"): "LAB_SOUTH_SHARED_REPORT",
             ("north", "notes"): "LAB_NORTH_SHARED_NOTES"}


def sign(tenant, document_id, expires, key):
    # Bind the complete resource scope and expiry using an unambiguous encoding.
    payload = ["download", tenant, document_id, expires]
    return hmac.new(key, json.dumps(payload, separators=(",", ":")).encode(), hashlib.sha256).hexdigest()


def redeem(tenant, document_id, expires, signature, key, now=NOW):
    if (not isinstance(tenant, str) or not isinstance(document_id, str)
            or type(expires) is not int or expires <= now
            or not isinstance(signature, str) or re.fullmatch(r"[0-9a-f]{64}", signature) is None):
        return {"status": 403}
    if not hmac.compare_digest(signature, sign(tenant, document_id, expires, key)):
        return {"status": 403}
    content = DOCUMENTS.get((tenant, document_id))
    return {"status": 404} if content is None else {"status": 200, "content": content}


def run(request):
    # A bounded flow: authenticated issuance, then redemption of the bearer link.
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    fields = ("issued_document_id", "requested_tenant", "requested_document_id")
    if any(not isinstance(request.get(k), str) or not 1 <= len(request[k]) <= 64 for k in fields):
        return {"status": 400}
    tenant = SESSIONS[token]
    issued_id = request["issued_document_id"]
    if (tenant, issued_id) not in DOCUMENTS:
        return {"status": 404}
    # Fresh server-owned key per flow; requests cannot choose it or the expiry.
    key = secrets.token_bytes(32)
    expires = NOW + 300
    signature = sign(tenant, issued_id, expires, key)
    return redeem(request["requested_tenant"], request["requested_document_id"], expires, signature, key)
