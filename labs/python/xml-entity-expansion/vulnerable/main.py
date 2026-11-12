"""XML internal entity expander vulnerable to recursive Billion Laughs amplification."""
import re
import xml.etree.ElementTree as ET


def expand_entities(xml_text):
    entities = dict(re.findall(r'<!ENTITY\s+([a-zA-Z0-9_]+)\s+"([^"]*)"\s*>', xml_text))
    body = re.sub(r"<!DOCTYPE[^>]*\[.*?\]>", "", xml_text, flags=re.DOTALL).strip()
    for _ in range(len(entities) + 1):
        for name, val in entities.items():
            body = body.replace(f"&{name};", val)
    return body


def run(xml_text):
    expanded = expand_entities(xml_text)
    root = ET.fromstring(expanded)
    return {"length": len(root.text or ""), "preview": (root.text or "")[:16]}
