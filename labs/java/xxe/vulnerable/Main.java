import javax.xml.parsers.*;
import org.xml.sax.InputSource;
import java.io.StringReader;
public class Main { public static void main(String[] args) throws Exception {
var factory=DocumentBuilderFactory.newInstance();
try { var doc=factory.newDocumentBuilder().parse(new InputSource(new StringReader(args[0]))); System.out.print(doc.getDocumentElement().getTextContent()); } catch(org.xml.sax.SAXException ex) {System.out.print("DENIED");}
}}