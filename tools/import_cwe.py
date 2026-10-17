#!/usr/bin/env python3
"""Import all weakness, category and view identifiers from an official CWE XML ZIP.

Usage: python3 tools/import_cwe.py /path/to/cwec_VERSION.xml.zip
The archive is deliberately supplied by the operator; tests never fetch the network.
"""
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def parse_archive(path):
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.endswith(".xml")]
        if len(names) != 1:
            raise ValueError("Expected exactly one XML file")
        raw = archive.read(names[0])
    root = ET.fromstring(raw)
    ns = {"cwe": root.tag.split("}")[0].strip("{")}
    entries = []
    for group, element, kind in [("Weaknesses", "Weakness", "weakness"),
                                  ("Categories", "Category", "category"), ("Views", "View", "view")]:
        for item in root.findall(f"cwe:{group}/cwe:{element}", ns):
            entries.append({"id": "CWE-" + item.attrib["ID"], "name": item.attrib["Name"],
                            "kind": kind, "status": item.attrib.get("Status", ""),
                            "abstraction": item.attrib.get("Abstraction", "")})
    entries.sort(key=lambda x: int(x["id"][4:]))
    return {"version": root.attrib["Version"], "date": root.attrib.get("Date"),
            "source": "https://cwe.mitre.org/data/downloads.html", "xml_sha256": hashlib.sha256(raw).hexdigest(),
            "license": "See THIRD_PARTY_NOTICES.md", "entries": entries}


if __name__ == "__main__":
    result = parse_archive(Path(sys.argv[1]))
    (ROOT / "catalog/cwe.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Imported CWE {result['version']}: {len(result['entries'])} entries")
