declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
const crypto = require("crypto");

function run(value: string): string {
    const expected = process.env.BADASS_ADMIN_PASSWORD;
    if (typeof expected !== "string" || !expected || typeof value !== "string") return "DENIED";
    const a = crypto.createHash("sha256").update(value, "utf8").digest();
    const b = crypto.createHash("sha256").update(expected, "utf8").digest();
    return value.length === expected.length && crypto.timingSafeEqual(a, b) ? "ADMIN" : "DENIED";
}
process.stdout.write(run(process.argv[2]));
