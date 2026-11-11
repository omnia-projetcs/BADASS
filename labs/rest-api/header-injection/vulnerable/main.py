"""REST API response builder that interpolates unvalidated input into headers."""


def evaluate(value):
    return "X-User: " + value + "\r\n\r\nBODY"


def run(request):
    return evaluate(request["value"])
