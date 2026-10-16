using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    if (value.Contains('\r') || value.Contains('\n')) return "DENIED";
    return "X-User: " + value + "\r\n\r\nBODY";
}
