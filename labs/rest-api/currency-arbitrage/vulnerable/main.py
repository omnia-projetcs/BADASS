"""Wallet top-up endpoint crediting raw payment amounts without currency normalization."""


def run(request):
    amount = request["amount"]
    if type(amount) is not int or amount < 10 or amount > 1000:
        return "DENIED"
    # Credits USD wallet with the raw numeric amount regardless of payment currency.
    return {"wallet_usd": 100 + amount, "charged_currency": request.get("currency", "USD")}
