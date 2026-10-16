using System;
using System.IO;
using System.Diagnostics;
var info = new ProcessStartInfo("/usr/bin/printf") { RedirectStandardOutput = true, UseShellExecute = false };
info.ArgumentList.Add("%s"); info.ArgumentList.Add(args[0]);
using var p = Process.Start(info)!; Console.Write(p.StandardOutput.ReadToEnd()); p.WaitForExit();
