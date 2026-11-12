// .NET XmlDocument parser forbidding DTD processing and nulling XmlResolver.
using System.Xml;

Console.Write(Run(args[0]));

static string Run(string xml) {
    try {
        var settings = new XmlReaderSettings {
            DtdProcessing = DtdProcessing.Prohibit,
            XmlResolver = null
        };
        using var reader = XmlReader.Create(new StringReader(xml), settings);
        var doc = new XmlDocument { XmlResolver = null };
        doc.Load(reader);
        return doc.DocumentElement?.InnerText ?? "";
    } catch {
        return "DENIED";
    }
}
