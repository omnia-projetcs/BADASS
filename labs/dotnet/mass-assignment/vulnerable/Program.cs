// .NET model binder deserializing directly into the domain entity including Role.
using System.Text.Json;

Console.Write(Run(args[0]));

static string Run(string raw) {
    using var doc = JsonDocument.Parse(raw);
    var root = doc.RootElement;
    var name = root.TryGetProperty("name", out var n) ? n.GetString() : "Alice";
    var role = root.TryGetProperty("role", out var r) ? r.GetString() : "user";
    return $"{name}:{role}";
}
