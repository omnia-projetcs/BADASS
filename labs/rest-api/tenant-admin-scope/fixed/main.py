"""Authorize administrative actions in the target account's own tenant."""
from copy import deepcopy
import json
from pathlib import Path


# Authentication and memberships are owned by the service, never by the body.
SESSIONS = {
    "LAB_NORTH_ADMIN": {"north": "admin", "south": "viewer"},
    "LAB_SOUTH_ADMIN": {"south": "admin"},
    "LAB_NORTH_VIEWER": {"north": "viewer"},
}
ACCOUNTS = {"north-member": {"tenant": "north", "active": True},
            "south-member": {"tenant": "south", "active": True}}


def disable(request, accounts):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    identifier = request.get("account_id")
    if not isinstance(identifier, str):
        return {"status": 400}
    target = accounts.get(identifier)
    if target is None:
        return {"status": 404}
    memberships = SESSIONS[token]
    # Resolve authority within the target account's server-owned tenant.
    if memberships.get(target["tenant"]) != "admin":
        return {"status": 403}
    target["active"] = False
    return {"status": 200, "disabled": identifier}


def run(request):
    accounts = deepcopy(ACCOUNTS)
    result = disable(request, accounts)
    Path("accounts-state.json").write_text(json.dumps(accounts, sort_keys=True) + "\n", encoding="utf-8")
    return result
