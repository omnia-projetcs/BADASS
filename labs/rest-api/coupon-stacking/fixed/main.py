"""REST API checkout handler enforcing single-use non-stackable coupons."""

COUPONS = {"WELCOME10": 10, "VIP30": 30}
MIN_TOTAL = 50


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    coupons = request.get("coupons", [])
    if not isinstance(coupons, list) or len(coupons) > 1:
        return "DENIED"
    subtotal = 100
    if coupons:
        code = coupons[0]
        if not isinstance(code, str) or code not in COUPONS:
            return "DENIED"
        subtotal -= COUPONS[code]
    if subtotal < MIN_TOTAL:
        return "DENIED"
    return {"status": 200, "total": subtotal}
