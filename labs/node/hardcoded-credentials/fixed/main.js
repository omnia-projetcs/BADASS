const crypto = require("crypto");

function run(value) {
    const expected = process.env.BADASS_ADMIN_PASSWORD;
    if (typeof expected !== "string" || !expected || typeof value !== "string") return "DENIED";
    const a = Buffer.from(value, "utf8");
    const b = Buffer.from(expected, "utf8");
    return a.length === b.length && crypto.timingSafeEqual(a, b) ? "ADMIN" : "DENIED";
}
process.stdout.write(run(process.argv[2]));
