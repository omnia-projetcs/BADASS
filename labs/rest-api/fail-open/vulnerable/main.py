"""REST API authorization guard that fails open on upstream connection errors."""


def evaluate(value):
    try:
        if value == "backend-down":
            raise ConnectionError("Authorization unavailable")
        return "ALLOWED" if value == "authorized" else "DENIED"
    except ConnectionError:
        return "ALLOWED"


def run(request):
    return evaluate(request["value"])
