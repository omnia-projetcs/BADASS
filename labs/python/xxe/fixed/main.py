"""Original SAX external-entity model inspired by EDB-43113."""
from io import StringIO
import xml.sax
from xml.sax.handler import ContentHandler, EntityResolver, LexicalHandler
from xml.sax.handler import feature_external_ges, property_lexical_handler


class TextHandler(ContentHandler, LexicalHandler):
    def __init__(self):
        super().__init__()
        self.parts = []

    def startDTD(self, name, public_id, system_id):
        # Parser-level rejection also covers internal and external subsets.
        raise xml.sax.SAXException("DTD is forbidden")

    def characters(self, text):
        self.parts.append(text)


class DenyEntities(EntityResolver):
    def resolveEntity(self, public_id, system_id):
        raise xml.sax.SAXException("external entities are forbidden")


def run(document):
    if not isinstance(document, str) or not 1 <= len(document) <= 4096:
        return {"status": 400, "error": "invalid XML"}
    handler = TextHandler()
    parser = xml.sax.make_parser()
    # External entities are disabled and every DTD is rejected explicitly.
    parser.setFeature(feature_external_ges, False)
    parser.setContentHandler(handler)
    parser.setProperty(property_lexical_handler, handler)
    parser.setEntityResolver(DenyEntities())
    try:
        parser.parse(StringIO(document))
    except (xml.sax.SAXException, OSError, ValueError, UnicodeError):
        return {"status": 400, "error": "invalid XML"}
    return {"status": 200, "text": "".join(handler.parts)}
