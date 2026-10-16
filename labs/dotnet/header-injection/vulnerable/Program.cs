using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    return "X-User: " + value + "\r\n\r\nBODY";
}
