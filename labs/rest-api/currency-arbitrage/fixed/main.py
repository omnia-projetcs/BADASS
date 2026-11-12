"""Wallet top-up endpoint enforcing strict USD settlement currency."""


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    amount = request.get("amount")
    currency = request.get("currency")
    if type(amount) is not int or not 10 <= amount <= 1000:
        return "DENIED"
    if currency != "USD":
        return "DENIED"
    return {"wallet_usd": 100 + amount, "charged_currency": "USD"}
