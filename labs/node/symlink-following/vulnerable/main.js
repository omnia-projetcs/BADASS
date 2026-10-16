function run(value) {
    const fs = require("node:fs");
    if (value === "preplaced-link") fs.symlinkSync("secret.txt", "export.tmp");
    let fd;
    try { fd = fs.openSync("export.tmp", "w", 0o600); }
    catch (error) { if (error.code !== "EEXIST") throw error; }
    if (fd !== undefined) {
        try { fs.writeFileSync(fd, "LAB_OVERWRITTEN"); } finally { fs.closeSync(fd); }
    }
    return fs.readFileSync("secret.txt", "utf8");
}
process.stdout.write(run(process.argv[2]));
