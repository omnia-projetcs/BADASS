"""Encode quotes as well as markup characters in a quoted HTML attribute."""
import html


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("value"), str):
        return {"status": 400, "error": "invalid value"}
    if len(request["value"]) > 2048:
        return {"status": 400, "error": "invalid value"}
    value = html.escape(request["value"], quote=True)
    return '<input value="' + value + '">'
