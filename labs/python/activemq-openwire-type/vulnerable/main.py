"""Decode a synthetic serialized throwable using an offline class registry."""
from pathlib import Path
import xml.etree.ElementTree as ET

CONTEXTS = {"lab://context": "<beans><marker>LAB_CONTEXT_LOADED</marker></beans>"}


class BrokerError(Exception):
    pass


class ContextLoader:
    def __init__(self, locator):
        document = ET.fromstring(CONTEXTS[locator])
        marker = document.findtext("marker")
        if marker is None: raise ValueError("missing marker")
        Path("loaded-context.txt").write_text(marker, encoding="utf-8")


CLASSES = {"BrokerError": BrokerError, "ContextLoader": ContextLoader}


def run(request):
    name, message = (request.get("class"), request.get("message")) if isinstance(request, dict) else (None, None)
    if not isinstance(name, str) or name not in CLASSES or not isinstance(message, str) or len(message) > 256:
        return {"status": 400, "error": "invalid throwable"}
    try:
        cls = CLASSES[name]
        pass
        obj = cls(message)
        if not isinstance(obj, Exception): return {"status": 400, "error": "invalid throwable"}
        return {"status": 200, "error_type": name, "message": str(obj)}
    except (KeyError, ValueError, ET.ParseError, UnicodeError):
        return {"status": 400, "error": "invalid throwable"}
