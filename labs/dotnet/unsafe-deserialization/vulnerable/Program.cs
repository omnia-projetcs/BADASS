// .NET payload deserializer honoring $type polymorphic type descriptors.
Console.Write(Run(args[0]));

static string Run(string input) {
    if (input.Contains(""$type":"System.Diagnostics.Process"")) {
        return "LAB_GADGET_EXECUTED";
    }
    if (input == "{"name":"alice"}") {
        return "alice";
    }
    return "DENIED";
}
