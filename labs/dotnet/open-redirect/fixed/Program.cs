using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    if (value != "/home" && value != "/profile") return "DENIED";
    return "Location: " + value;
}
