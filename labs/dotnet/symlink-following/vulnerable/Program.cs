using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    if (value == "preplaced-link") File.CreateSymbolicLink("export.tmp", "secret.txt");
    try {
        using var stream = File.Open("export.tmp", FileMode.Create, FileAccess.Write);
        stream.Write(Encoding.UTF8.GetBytes("LAB_OVERWRITTEN"));
    } catch (IOException) when (File.Exists("export.tmp")) {
        // The exclusive-create path leaves an existing file or symlink untouched.
    }
    return File.ReadAllText("secret.txt");
}
