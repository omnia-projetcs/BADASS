using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    int quantity = int.Parse(value);
    return (1000 - quantity * 10).ToString();
}
