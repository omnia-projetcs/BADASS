import javax.xml.parsers.*;
import org.xml.sax.InputSource;
import java.io.StringReader;
public class Main { public static void main(String[] args) throws Exception {
var factory=DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setAttribute(javax.xml.XMLConstants.ACCESS_EXTERNAL_DTD, "");
factory.setAttribute(javax.xml.XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
try { var doc=factory.newDocumentBuilder().parse(new InputSource(new StringReader(args[0]))); System.out.print(doc.getDocumentElement().getTextContent()); } catch(org.xml.sax.SAXException ex) {System.out.print("DENIED");}
}}