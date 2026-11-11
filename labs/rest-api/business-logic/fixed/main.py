"""REST API order pricing endpoint with quantity range validation."""


def evaluate(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return "DENIED"
    if isinstance(value, str) and (len(value) > 16 or value.strip().startswith("-0")):
        return "DENIED"
    try:
        quantity = int(value)
    except ValueError:
        return "DENIED"
    if not 1 <= quantity <= 100:
        return "DENIED"
    return str(1000 - quantity * 10)


def run(request):
    if not isinstance(request, dict) or "value" not in request:
        return "DENIED"
    return evaluate(request["value"])
