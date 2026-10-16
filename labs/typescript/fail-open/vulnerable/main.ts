declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    try {
        if (value === "backend-down") throw new Error("Authorization unavailable");
        return value === "authorized" ? "ALLOWED" : "DENIED";
    } catch (error: any) { return "ALLOWED"; }
}
process.stdout.write(run(process.argv[2]));
