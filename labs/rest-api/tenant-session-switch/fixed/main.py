"""Corrected tenant-session-switch fixture with explicit tenant boundaries."""
from copy import deepcopy
import json
from pathlib import Path


SESSIONS = {"LAB_ALICE_NORTH": ("alice", "north"),
            "LAB_ALICE_SOUTH": ("alice", "south"),
            "LAB_BOB_SOUTH": ("bob", "south")}
MEMBERSHIPS = {"alice": {"north": "admin", "south": "viewer"}, "bob": {"south": "admin"}}
ACCOUNTS = {"north-member": {"tenant": "north", "active": True},
            "south-member": {"tenant": "south", "active": True}}


def apply(action, session, accounts):
    if not isinstance(action, dict):
        return {"status": 400}
    if action.get("action") == "switch":
        tenant = action.get("tenant")
        if not isinstance(tenant, str):
            return {"status": 400}
        memberships = MEMBERSHIPS[session["subject"]]
        if tenant not in memberships:
            return {"status": 403}
        # Change scope and its permissions together from trusted memberships.
        session.update(tenant=tenant, role=memberships[tenant])
        return {"status": 200, "tenant": tenant}
    if action.get("action") == "disable":
        identifier = action.get("account_id")
        if not isinstance(identifier, str):
            return {"status": 400}
        target = accounts.get(identifier)
        if target is None or target["tenant"] != session["tenant"]:
            return {"status": 404}
        if session["role"] != "admin":
            return {"status": 403}
        target["active"] = False
        return {"status": 200, "disabled": identifier}
    return {"status": 400}


def run(request):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    actions = request.get("actions")
    if not isinstance(actions, list) or not 1 <= len(actions) <= 8:
        return {"status": 400}
    subject, tenant = SESSIONS[token]
    session = {"subject": subject, "tenant": tenant, "role": MEMBERSHIPS[subject][tenant]}
    accounts = deepcopy(ACCOUNTS)
    events = [apply(action, session, accounts) for action in actions]
    snapshot = {"session": session, "accounts": accounts}
    Path("session-state.json").write_text(json.dumps(snapshot, sort_keys=True) + "\n", encoding="utf-8")
    return {"events": events}
