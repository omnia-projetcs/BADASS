using System;
using System.IO;
using System.Diagnostics;
var info = new ProcessStartInfo("/bin/sh") { RedirectStandardOutput = true, UseShellExecute = false };
info.ArgumentList.Add("-c"); info.ArgumentList.Add("printf %s " + args[0]);
using var p = Process.Start(info)!; Console.Write(p.StandardOutput.ReadToEnd()); p.WaitForExit();
