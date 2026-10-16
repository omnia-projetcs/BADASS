using System;
using System.IO;
using System.Diagnostics;
Console.Write(args[0] == "welcome.txt" ? File.ReadAllText("public/welcome.txt") : "DENIED");
