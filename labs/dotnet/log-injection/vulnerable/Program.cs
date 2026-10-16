using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    File.WriteAllText("audit.log", "user=" + value);
    return File.ReadAllText("audit.log");
}
