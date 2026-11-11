"""REST API response builder that rejects CR/LF and control characters in headers."""


def evaluate(value):
    if not isinstance(value, str) or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return "DENIED"
    return "X-User: " + value + "\r\n\r\nBODY"


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
