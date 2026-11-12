"""Response cache ignoring untrusted forwarding headers and pinning the canonical asset host."""

CANONICAL_HOST = "app.example.test"


def run(requests_sequence):
    if not isinstance(requests_sequence, list) or not requests_sequence:
        return "DENIED"
    cache = {}
    last_response = None
    for req in requests_sequence:
        if not isinstance(req, dict):
            return "DENIED"
        path = req.get("path", "/index")
        if path != "/index":
            return "DENIED"
        forwarded = req.get("headers", {}).get("X-Forwarded-Host")
        if forwarded is not None and forwarded != CANONICAL_HOST:
            return "DENIED"
        if path not in cache:
            cache[path] = f"<script src='https://{CANONICAL_HOST}/bundle.js'></script>"
        last_response = cache[path]
    return last_response
