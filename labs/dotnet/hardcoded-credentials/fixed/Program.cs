using System.Security.Cryptography;
using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    string? expected = Environment.GetEnvironmentVariable("BADASS_ADMIN_PASSWORD");
    if (string.IsNullOrEmpty(expected) || value is null) return "DENIED";
    byte[] expectedBytes = Encoding.UTF8.GetBytes(expected);
    byte[] suppliedBytes = Encoding.UTF8.GetBytes(value);
    return CryptographicOperations.FixedTimeEquals(expectedBytes, suppliedBytes) ? "ADMIN" : "DENIED";
}
