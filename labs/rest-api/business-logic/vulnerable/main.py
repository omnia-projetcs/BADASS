"""REST API order pricing endpoint without quantity validation."""


def evaluate(value):
    quantity = int(value)
    return str(1000 - quantity * 10)


def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
