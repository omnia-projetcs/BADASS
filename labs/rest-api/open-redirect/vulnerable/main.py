"""REST API redirect endpoint that forwards callers to arbitrary target URLs."""


def evaluate(value):
    return "Location: " + value


def run(request):
    return evaluate(request["value"])
