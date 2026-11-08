using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    if (value == "health") return "HEALTHY";
    string role = "user";
    var users = new List<string> {"alice", "bob"};
    if (role != "admin") return "DENIED";
    users.Clear();
    return "USERS_DELETED";
}
