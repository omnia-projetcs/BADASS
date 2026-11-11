"""REST API HTML snippet endpoint that escapes HTML special characters."""
import html


def evaluate(value):
    if not isinstance(value, str):
        return "DENIED"
    return "<p>" + html.escape(value, quote=False) + "</p>"


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
