"""Batch payout splitter using exact integer division and remainder allocation."""


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    total_cents = request.get("total_cents")
    splits = request.get("splits")
    if type(total_cents) is not int or type(splits) is not int:
        return "DENIED"
    if not (1 <= total_cents <= 100000 and 1 <= splits <= 100):
        return "DENIED"
    base, remainder = divmod(total_cents, splits)
    payouts = [base + (1 if i < remainder else 0) for i in range(splits)]
    if sum(payouts) != total_cents:
        return "DENIED"
    return {"debited": total_cents, "credited": sum(payouts), "payouts": payouts}
