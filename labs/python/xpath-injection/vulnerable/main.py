"""XML account query concatenating untrusted input into an ElementTree XPath expression."""
import xml.etree.ElementTree as ET

XML_DOC = """<accounts>
  <account user="alice" role="user"><secret>ALICE_NOTE</secret></account>
  <account user="admin" role="admin"><secret>LAB_ADMIN_SECRET</secret></account>
</accounts>"""


def run(user):
    root = ET.fromstring(XML_DOC)
    node = root.find(f".//account[@user='{user}']/secret")
    return node.text if node is not None else "NOT_FOUND"
