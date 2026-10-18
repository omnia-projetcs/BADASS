"""Original SAX external-entity model inspired by EDB-43113."""
from io import StringIO
from pathlib import Path
from urllib.parse import unquote, urlsplit
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


class LocalEntities(EntityResolver):
    def resolveEntity(self, public_id, system_id):
        uri = urlsplit(system_id)
        # The teaching fixture deliberately models file disclosure only.
        if uri.scheme not in {"", "file"} or uri.netloc or uri.query or uri.fragment:
            raise xml.sax.SAXException("network entities are outside this fixture")
        return str(Path(unquote(uri.path)).resolve())


def run(document):
    if not isinstance(document, str) or not 1 <= len(document) <= 4096:
        return {"status": 400, "error": "invalid XML"}
    handler = TextHandler()
    parser = xml.sax.make_parser()
    # External entities are disabled and every DTD is rejected explicitly.
    parser.setFeature(feature_external_ges, False)
    parser.setContentHandler(handler)
    parser.setProperty(property_lexical_handler, handler)
    parser.setEntityResolver(LocalEntities())
    try:
        parser.parse(StringIO(document))
    except (xml.sax.SAXException, OSError, ValueError, UnicodeError):
        return {"status": 400, "error": "invalid XML"}
    return {"status": 200, "text": "".join(handler.parts)}
