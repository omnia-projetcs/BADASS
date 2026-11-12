Console.Write(Run(args[0]));

static string Run(string value) {
    if (string.IsNullOrEmpty(value) || value.StartsWith('-') || value.StartsWith('+')) return "DENIED";
    if (!int.TryParse(value, out int quantity) || quantity < 1 || quantity > 100) return "DENIED";
    return (1000 - quantity * 10).ToString();
}
