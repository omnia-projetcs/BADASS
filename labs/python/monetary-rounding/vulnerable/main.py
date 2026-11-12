"""Batch payout splitter using upward floating-point rounding that mints extra cents."""
import math


def run(request):
    total_cents = request["total_cents"]
    splits = request["splits"]
    share = math.ceil(float(total_cents) / float(splits))
    payouts = [share] * splits
    return {"debited": total_cents, "credited": sum(payouts), "payouts": payouts}
