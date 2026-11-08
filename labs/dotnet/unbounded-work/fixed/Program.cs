using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    int size = int.Parse(value);
    if (size < 0) throw new ArgumentOutOfRangeException(nameof(value));
    if (size > 100) return "DENIED";
    var data = new byte[size];
    return data.Length.ToString();
}
