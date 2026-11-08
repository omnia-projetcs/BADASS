using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    int quantity = int.Parse(value);
    if (quantity < 1 || quantity > 100) return "DENIED";
    return (1000 - quantity * 10).ToString();
}
