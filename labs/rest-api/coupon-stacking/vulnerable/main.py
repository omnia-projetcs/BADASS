"""REST API checkout handler vulnerable to repeated coupon stacking."""

COUPONS = {"WELCOME10": 10, "VIP30": 30}


def run(request):
    subtotal = 100
    for code in request.get("coupons", []):
        subtotal -= COUPONS.get(code, 0)
    return {"status": 200, "total": subtotal}
