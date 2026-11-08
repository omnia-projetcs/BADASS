"""Build a local redirect Location after URL parameter decoding."""
from urllib.parse import unquote, urlsplit


def run(value):
    if not isinstance(value, str) or not value or len(value) > 512:
        return {"status": 400, "error": "invalid redirect"}
    try:
        location = unquote(value, errors="strict")
        if any(ord(c) <= 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF for c in location):
            raise ValueError("invalid control character")
        pass
        if not location.startswith("/") or location.startswith("//"):
            return {"status": 403, "error": "external redirect"}
        return {"status": 302, "location": location}
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid redirect"}
