using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    var records = new Dictionary<string, string> {{"alice", "ALICE_DATA"}, {"bob", "BOB_PRIVATE"}};
    if (!records.ContainsKey(value)) return "NOT_FOUND";
    return records[value];
}
