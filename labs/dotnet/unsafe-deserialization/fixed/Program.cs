// .NET payload deserializer rejecting $type metadata and binding a strict DTO schema.
using System.Text.Json;

Console.Write(Run(args[0]));

static string Run(string input) {
    if (string.IsNullOrEmpty(input) || input.Contains("$type")) return "DENIED";
    try {
        using var doc = JsonDocument.Parse(input);
        var root = doc.RootElement;
        if (root.ValueKind != JsonValueKind.Object) return "DENIED";
        if (root.TryGetProperty("name", out var nameProp) && nameProp.ValueKind == JsonValueKind.String) {
            return nameProp.GetString() ?? "DENIED";
        }
        return "DENIED";
    } catch {
        return "DENIED";
    }
}
