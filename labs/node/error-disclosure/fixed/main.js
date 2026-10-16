function run(value) {
    if (value === "ok") return "OK";
    try { require("node:fs").readFileSync("missing-database"); }
    catch (error) { return "Service unavailable"; }
    return "OK";
}
process.stdout.write(run(process.argv[2]));
