"""A server-owned state machine permits payment followed by one delivery."""
import json
from pathlib import Path


def run(request):
    # One invocation contains the successive actions of one isolated session.
    if not isinstance(request, dict) or not isinstance(request.get("actions"), list):
        return {"status": 400, "error": "invalid actions"}
    actions = request["actions"]
    if len(actions) > 8 or any(action not in ("pay", "deliver") for action in actions):
        return {"status": 400, "error": "invalid actions"}

    # All payment and order state is server-owned. Client fields named paid,
    # state, price, or balance cannot initialize it. No real payment is made.
    # This bounded, single-process fixture does not claim concurrent durability.
    order = {"state": "created", "charged_cents": 0, "charges": 0, "shipments": 0}
    events = []
    for action in actions:
        if action == "pay":
            if order["state"] != "created":
                events.append({"action": action, "status": 409})
                continue
            with Path("payments.log").open("a", encoding="utf-8") as ledger:
                ledger.write("LAB_ORDER_1:1000\n")
            order.update(state="paid", charged_cents=1000, charges=1)
        else:
            if order["state"] != "paid":
                events.append({"action": action, "status": 409})
                continue
            with Path("shipments.log").open("a", encoding="utf-8") as ledger:
                ledger.write("LAB_ORDER_1\n")
            order["shipments"] += 1
            order["state"] = "delivered"
        events.append({"action": action, "status": 200})

    Path("order-state.json").write_text(json.dumps(order, sort_keys=True) + "\n", encoding="utf-8")
    return {"status": 200, "events": events, "order": order}
