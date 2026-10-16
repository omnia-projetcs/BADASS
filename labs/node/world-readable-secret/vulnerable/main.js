function run(value) {
    const fs = require("node:fs");
    const fd = fs.openSync("stored-secret", "wx", 0o600);
    try {
        fs.writeFileSync(fd, value === "public" ? "PUBLIC" : "LAB_SECRET");
        fs.fchmodSync(fd, 0o644);
        return (fs.fstatSync(fd).mode & 0o777).toString(8).padStart(4, "0");
    } finally { fs.closeSync(fd); }
}
process.stdout.write(run(process.argv[2]));
