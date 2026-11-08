"""Text-context escaping leaves a quoted HTML attribute open to injection."""
import html


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("value"), str):
        return {"status": 400, "error": "invalid value"}
    if len(request["value"]) > 2048:
        return {"status": 400, "error": "invalid value"}
    value = html.escape(request["value"], quote=False)
    return '<input value="' + value + '">'
