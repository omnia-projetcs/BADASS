"""REST API allocation endpoint with strict size validation."""


def evaluate(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return "DENIED"
    if isinstance(value, str) and (len(value) > 16 or value.strip().startswith("-0")):
        return "DENIED"
    try:
        size = int(value)
    except ValueError:
        return "DENIED"
    if not 0 <= size <= 100:
        return "DENIED"
    return str(len(bytearray(size)))


def run(request):
    if not isinstance(request, dict) or "value" not in request:
        return "DENIED"
    return evaluate(request["value"])
