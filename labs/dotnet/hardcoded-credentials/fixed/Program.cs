using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    string? expected = Environment.GetEnvironmentVariable("BADASS_ADMIN_PASSWORD");
    return !string.IsNullOrEmpty(expected) && value == expected ? "ADMIN" : "DENIED";
}
