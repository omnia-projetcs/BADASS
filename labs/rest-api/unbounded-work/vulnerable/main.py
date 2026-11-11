"""REST API allocation endpoint without upper bounds on requested size."""


def evaluate(value):
    size = int(value)
    return str(len(bytearray(size)))


def run(request):
    return evaluate(request["value"])
