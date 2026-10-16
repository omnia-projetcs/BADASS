using System.Text;

Console.Write(Run(args[0]));

static string Run(string value) {
    var ownerOnly = UnixFileMode.UserRead | UnixFileMode.UserWrite;
    using (var stream = File.Open("stored-secret", new FileStreamOptions {Mode = FileMode.CreateNew, Access = FileAccess.Write, UnixCreateMode = ownerOnly})) {
        byte[] bytes = Encoding.UTF8.GetBytes(value == "public" ? "PUBLIC" : "LAB_SECRET");
        stream.Write(bytes);
    }
    var mode = ownerOnly | UnixFileMode.GroupRead | UnixFileMode.OtherRead;
    if (value == "secret") mode = ownerOnly;
    File.SetUnixFileMode("stored-secret", mode);
    return Convert.ToString((int)File.GetUnixFileMode("stored-secret"), 8).PadLeft(4, '0');
}
