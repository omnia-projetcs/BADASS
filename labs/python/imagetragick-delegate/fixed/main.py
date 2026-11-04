"""Parse an SVG resource and invoke a local echo-only delegate."""
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit


def run(document):
    if not isinstance(document, str) or len(document) > 2048 or "<!DOCTYPE" in document.upper() or "<!ENTITY" in document.upper():
        return {"status": 400, "error": "invalid image resource"}
    try:
        root = ET.fromstring(document)
        resources = [node.attrib["href"] for node in root.iter("{http://www.w3.org/2000/svg}image") if "href" in node.attrib]
        if root.tag != "{http://www.w3.org/2000/svg}svg" or len(resources) != 1:
            raise ValueError("one resource required")
        url = resources[0]
        if len(url) > 512 or any(ord(c) < 32 for c in url) or urlsplit(url).scheme != "https" or not urlsplit(url).hostname:
            raise ValueError("invalid resource")
        result = subprocess.run(["/usr/bin/printf", "%s", url], shell=False,
                                capture_output=True, text=True, timeout=2)
        if result.returncode != 0: raise ValueError("delegate failure")
        return {"status": 200, "echo": result.stdout}
    except (ET.ParseError, ValueError, UnicodeError, subprocess.SubprocessError):
        return {"status": 400, "error": "invalid image resource"}
