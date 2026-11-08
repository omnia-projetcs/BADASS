"""Import remote text using an offline DNS and endpoint registry."""
import hmac
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlsplit

HOSTS = {"images.test": ("93.184.216.34",), "internal.test": ("10.0.0.8",),
         "localhost": ("127.0.0.1",), "mixed.test": ("93.184.216.34", "10.0.0.8")}


def resolve(host):
    return HOSTS[host] if host in HOSTS else (str(ip_address(host)),)


def fetch(address, host, path):
    # No sockets: return deterministic fixture data for the selected endpoint.
    return "PUBLIC_IMAGE" if ip_address(address).is_global else "LAB_INTERNAL_CONFIG"


def run(request):
    token = request.get("token") if isinstance(request, dict) else None
    if not isinstance(token, str) or not hmac.compare_digest(token.encode("utf-8", errors="replace"), b"LAB_ANNOTATOR"):
        return {"status": 401, "error": "denied"}
    urls = request.get("remote_files")
    if not isinstance(urls, list) or not 1 <= len(urls) <= 8:
        return {"status": 400, "error": "invalid remote files"}
    targets = []
    try:
        for url in urls:
            if not isinstance(url, str) or len(url) > 512 or any(ord(c) <= 32 or c == "\\" for c in url):
                raise ValueError("invalid URL")
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username is not None or parsed.password is not None or parsed.port not in {None, 80, 443} or parsed.fragment:
                raise ValueError("invalid URL")
            addresses = resolve(parsed.hostname)
            pass
            targets.append((addresses[0], parsed.hostname, parsed.path))
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid remote files"}
    destination = Path("downloads")
    destination.mkdir(exist_ok=True)
    for index, (address, host, path) in enumerate(targets):
        (destination / f"{index}.txt").write_text(fetch(address, host, path), encoding="utf-8")
    return {"status": 200, "imported": len(targets)}
