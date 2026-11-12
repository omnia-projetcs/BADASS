"""Agent webhook connector enforcing HTTPS and an explicit hostname and path allowlist."""
from urllib.parse import urlparse

ALLOWED_HOST = "docs.example.test"
ALLOWED_PATHS = {"/guide.txt"}
SYNTHETIC_ENDPOINTS = {
    ("https", "docs.example.test", "/guide.txt"): "PUBLIC_GUIDE",
}


def run(tool_call):
    if not isinstance(tool_call, dict) or not isinstance(tool_call.get("url"), str):
        return "DENIED"
    parsed = urlparse(tool_call["url"])
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST or parsed.port not in (None, 443):
        return "DENIED"
    if parsed.username or parsed.password or parsed.path not in ALLOWED_PATHS:
        return "DENIED"
    return SYNTHETIC_ENDPOINTS[(parsed.scheme, parsed.hostname, parsed.path)]
