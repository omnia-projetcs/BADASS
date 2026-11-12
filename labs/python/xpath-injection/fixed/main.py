"""XML account query enforcing strict identifier validation and safe attribute comparison."""
import re
import xml.etree.ElementTree as ET

XML_DOC = """<accounts>
  <account user="alice" role="user"><secret>ALICE_NOTE</secret></account>
  <account user="admin" role="admin"><secret>LAB_ADMIN_SECRET</secret></account>
</accounts>"""


def run(user):
    if not isinstance(user, str) or not re.fullmatch(r"[a-z]{1,16}", user) or user == "admin":
        return "DENIED"
    root = ET.fromstring(XML_DOC)
    for account in root.findall("account"):
        if account.attrib.get("user") == user and account.attrib.get("role") == "user":
            secret = account.find("secret")
            return secret.text if secret is not None else "NOT_FOUND"
    return "NOT_FOUND"
