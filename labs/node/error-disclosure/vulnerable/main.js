function run(value) {
    if (value === "ok") return "OK";
    try { require("node:fs").readFileSync("missing-database"); }
    catch (error) { return "db://admin:LAB_SECRET@database/internal"; }
    return "OK";
}
process.stdout.write(run(process.argv[2]));
