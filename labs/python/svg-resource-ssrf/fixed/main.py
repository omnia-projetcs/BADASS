"""Inspect uploaded SVG image resources with an offline fetch dependency."""
import hmac
import xml.etree.ElementTree as ET

ENDPOINTS = {
    "https://images.test/logo.png": "PUBLIC_IMAGE",
    "http://127.0.0.1/config": "LAB_INTERNAL_CONFIG",
    "http://169.254.169.254/metadata": "LAB_METADATA",
}


def fetch(url):
    return ENDPOINTS[url]


def run(request):
    token = request.get("token") if isinstance(request, dict) else None
    if not isinstance(token, str) or not hmac.compare_digest(token.encode("utf-8", errors="replace"), b"LAB_TENANT_ADMIN"):
        return {"status": 401, "error": "denied"}
    document = request.get("svg")
    if not isinstance(document, str) or len(document) > 4096 or "<!DOCTYPE" in document.upper() or "<!ENTITY" in document.upper():
        return {"status": 400, "error": "invalid SVG"}
    try:
        root = ET.fromstring(document)
        if root.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError("SVG root required")
        resources = [value for node in root.iter() for key, value in node.attrib.items()
                     if key in {"href", "{http://www.w3.org/1999/xlink}href"} and not value.startswith("#")]
        if len(resources) > 8:
            raise ValueError("too many resources")
        if resources:
            return {"status": 403, "error": "external SVG resource"}
        return {"status": 200, "resources": [fetch(url) for url in resources]}
    except (ET.ParseError, ValueError, KeyError, UnicodeError):
        return {"status": 400, "error": "invalid SVG"}
