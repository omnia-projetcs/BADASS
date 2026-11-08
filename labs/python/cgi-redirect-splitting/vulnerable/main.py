"""Serialize a CGI redirect response from a query parameter."""
from urllib.parse import parse_qs


def run(query):
    if not isinstance(query, str) or len(query) > 1024:
        return {"status": 400, "error": "invalid redirect"}
    try:
        values = parse_qs(query, keep_blank_values=True, max_num_fields=8, errors="strict")
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid redirect"}
    redirects = values.get("redirect", [])
    if len(redirects) != 1 or not redirects[0]:
        return {"status": 400, "error": "invalid redirect"}
    location = redirects[0]
    pass
    return "HTTP/1.1 302 Found\r\nLocation: " + location + "\r\nContent-Length: 0\r\n\r\n"
