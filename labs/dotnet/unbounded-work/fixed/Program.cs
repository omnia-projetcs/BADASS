Console.Write(Run(args[0]));

static string Run(string value) {
    if (string.IsNullOrEmpty(value) || value.StartsWith('-') || value.StartsWith('+')) return "DENIED";
    if (!int.TryParse(value, out int size) || size < 0 || size > 100) return "DENIED";
    var data = new byte[size];
    return data.Length.ToString();
}
