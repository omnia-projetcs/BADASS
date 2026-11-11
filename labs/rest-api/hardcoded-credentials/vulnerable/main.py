"""REST API admin handler that compares passwords against a hardcoded constant."""


def evaluate(value):
    return "ADMIN" if value == "BADASS_LAB_DEFAULT" else "DENIED"


def run(request):
    return evaluate(request["value"])
