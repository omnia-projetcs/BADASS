"""Exercise resolve-before-connect policy with an offline transport."""
from ipaddress import ip_address
from urllib.parse import urlsplit

ANSWERS = {
    "images.test": [("93.184.216.34",)],
    "rebind.test": [("93.184.216.34",), ("127.0.0.1",)],
    "metadata.test": [("93.184.216.34",), ("169.254.169.254",)],
    "mixed.test": [("93.184.216.34", "127.0.0.1")],
    "localhost": [("127.0.0.1",)],
}


class Resolver:
    def __init__(self):
        self.calls = 0

    def resolve(self, host):
        answers = ANSWERS.get(host)
        if answers is None:
            answers = [(str(ip_address(host)),)]
        result = answers[min(self.calls, len(answers) - 1)]
        self.calls += 1
        return result


def is_public_address(raw):
    address = ip_address(raw)
    if getattr(address, "ipv4_mapped", None) is not None:
        address = address.ipv4_mapped
    if address.version == 6 and int(address) >> 32 == 0x0064FF9B0000000000000000:
        return False
    return address.is_global and not (
        address.is_multicast or address.is_reserved or address.is_unspecified
        or address.is_loopback or address.is_link_local or address.is_private
    )


def connect(address, host, path):
    # This function is an offline endpoint registry, never a socket call.
    return "PUBLIC_IMAGE" if is_public_address(address) else "LAB_INTERNAL_SERVICE"


def run(url):
    if not isinstance(url, str) or len(url) > 512 or any(ord(c) <= 32 or c == "\\" for c in url):
        return {"status": 400, "error": "invalid URL"}
    try:
        target = urlsplit(url)
        if target.scheme not in {"http", "https"} or not target.hostname or target.username is not None or target.password is not None or target.port not in {None, 80, 443} or target.fragment:
            raise ValueError("invalid URL")
        resolver = Resolver()
        addresses = resolver.resolve(target.hostname)
        if not addresses or not all(is_public_address(item) for item in addresses):
            return {"status": 403, "error": "internal destination"}
        address = addresses[0]
        return {"status": 200, "body": connect(address, target.hostname, target.path)}
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid URL"}
