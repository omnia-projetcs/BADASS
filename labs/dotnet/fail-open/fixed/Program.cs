using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    try {
        if (value == "backend-down") throw new IOException("Authorization unavailable");
        return value == "authorized" ? "ALLOWED" : "DENIED";
    } catch (IOException) { return "DENIED"; }
}
