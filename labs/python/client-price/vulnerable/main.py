"""Checkout relies on the price supplied by the client's product selector."""
import json
from pathlib import Path


PRICES = {"book": 120, "lamp": 250}


def quote(request, prices=None, balance=1000):
    prices = PRICES if prices is None else prices
    if not isinstance(request, dict) or not isinstance(request.get("product"), str):
        return {"status": 400}
    product = request["product"]
    quantity, supplied_price = request.get("quantity"), request.get("unit_price")
    if (type(quantity) not in (int, float) or not 1 <= quantity <= 5 or quantity % 1 != 0
            or type(supplied_price) not in (int, float) or not 0 <= supplied_price <= 10000 or supplied_price % 1 != 0):
        return {"status": 400}
    if product not in prices:
        return {"status": 404}
    quantity = int(quantity)
    # The browser's read-only price field is incorrectly treated as authoritative.
    unit_price = int(supplied_price)
    total = quantity * unit_price
    if total > balance:
        return {"status": 402}
    return {"status": 201, "receipt": {"product": product, "quantity": quantity,
            "unit_price": unit_price, "total": total, "remaining": balance - total}}


def run(request):
    result = quote(request)
    if result["status"] != 201:
        return result
    receipt = result["receipt"]
    Path("order.json").write_text(json.dumps(receipt, separators=(",", ":")) + "\n", encoding="utf-8")
    return {"status": 201, "total": receipt["total"], "remaining": receipt["remaining"]}
