using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    value = value.Replace("\\", "\\\\").Replace("\r", "\\r").Replace("\n", "\\n");
    File.WriteAllText("audit.log", "user=" + value);
    return File.ReadAllText("audit.log");
}
