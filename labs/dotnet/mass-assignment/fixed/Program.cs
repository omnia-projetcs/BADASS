// .NET model binder binding only the allowlisted Name property into a DTO.
using System.Text.Json;

Console.Write(Run(args[0]));

static string Run(string raw) {
    try {
        using var doc = JsonDocument.Parse(raw);
        var root = doc.RootElement;
        var name = root.TryGetProperty("name", out var n) && n.ValueKind == JsonValueKind.String ? n.GetString() : "Alice";
        return $"{name}:user";
    } catch {
        return "DENIED";
    }
}
