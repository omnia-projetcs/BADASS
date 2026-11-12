"""Response cache keying only on path while reflecting unkeyed X-Forwarded-Host headers."""


def run(requests_sequence):
    cache = {}
    last_response = None
    for req in requests_sequence:
        path = req.get("path", "/index")
        if path not in cache:
            host = req.get("headers", {}).get("X-Forwarded-Host", "app.example.test")
            cache[path] = f"<script src='https://{host}/bundle.js'></script>"
        last_response = cache[path]
    return last_response
