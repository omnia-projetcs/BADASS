"""REST API HTML snippet endpoint that reflects unescaped input."""


def evaluate(value):
    return "<p>" + value + "</p>"


def run(request):
    return evaluate(request["value"])
