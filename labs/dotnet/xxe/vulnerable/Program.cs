// .NET XmlDocument parser with DtdProcessing.Parse and XmlUrlResolver enabled.
using System.Xml;

Console.Write(Run(args[0]));

static string Run(string xml) {
    var settings = new XmlReaderSettings {
        DtdProcessing = DtdProcessing.Parse,
        XmlResolver = new XmlUrlResolver()
    };
    using var reader = XmlReader.Create(new StringReader(xml), settings);
    var doc = new XmlDocument { XmlResolver = new XmlUrlResolver() };
    doc.Load(reader);
    return doc.DocumentElement?.InnerText ?? "";
}
