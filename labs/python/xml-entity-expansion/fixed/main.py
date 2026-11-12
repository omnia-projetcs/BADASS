"""XML parser rejecting DOCTYPE and ENTITY declarations and bounding document size."""
import xml.etree.ElementTree as ET


def run(xml_text):
    if not isinstance(xml_text, str) or len(xml_text) > 1024:
        return "DENIED"
    upper = xml_text.upper()
    if "<!DOCTYPE" in upper or "<!ENTITY" in upper:
        return "DENIED"
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return "DENIED"
    text = root.text or ""
    if len(text) > 256:
        return "DENIED"
    return {"length": len(text), "preview": text[:16]}
