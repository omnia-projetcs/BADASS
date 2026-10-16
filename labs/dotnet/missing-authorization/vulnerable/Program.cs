using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    if (value == "health") return "HEALTHY";
    string role = "user";
    var users = new List<string> {"alice", "bob"};
    users.Clear();
    return "USERS_DELETED";
}
