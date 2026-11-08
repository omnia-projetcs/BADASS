"""Authorize the selected invoice using the tenant from the server session."""

# This server-owned table represents authenticated middleware state. Request
# fields such as tenant_id and role are never accepted as authenticated context.
SESSION_STORE = {
    "LAB_ALICE_SESSION": {"subject": "alice", "tenant_id": "north"},
    "LAB_BOB_SESSION": {"subject": "bob", "tenant_id": "south"},
}
INVOICES = {
    "invoice-north": {"id": "invoice-north", "tenant_id": "north", "total": 10,
                      "memo": "LAB_NORTH_INVOICE"},
    "invoice-south": {"id": "invoice-south", "tenant_id": "south", "total": 900,
                      "memo": "LAB_SOUTH_INVOICE"},
}


def run(request):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSION_STORE:
        return {"status": 401}
    principal = SESSION_STORE[token]
    invoice_id = request.get("invoice_id")
    if not isinstance(invoice_id, str):
        return {"status": 400}
    invoice = INVOICES.get(invoice_id)
    if invoice is None or invoice["tenant_id"] != principal["tenant_id"]:
        return {"status": 404}
    return {"status": 200, "body": dict(invoice)}
