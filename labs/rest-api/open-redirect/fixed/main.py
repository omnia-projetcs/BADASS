"""REST API redirect endpoint restricted to allowlisted local destinations."""


def evaluate(value):
    if not isinstance(value, str) or value not in {"/home", "/profile"}:
        return "DENIED"
    return "Location: " + value


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
