using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    if (value == "ok") return "OK";
    try { File.ReadAllText("missing-database"); }
    catch (FileNotFoundException) { return "Service unavailable"; }
    return "OK";
}
