declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    if (value === "ok") return "OK";
    try { require("node:fs").readFileSync("missing-database"); }
    catch (error: any) { return "db://admin:LAB_SECRET@database/internal"; }
    return "OK";
}
process.stdout.write(run(process.argv[2]));
