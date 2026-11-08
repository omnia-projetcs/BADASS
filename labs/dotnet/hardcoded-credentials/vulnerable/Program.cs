using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    string? expected = "BADASS_LAB_DEFAULT";
    return !string.IsNullOrEmpty(expected) && value == expected ? "ADMIN" : "DENIED";
}
