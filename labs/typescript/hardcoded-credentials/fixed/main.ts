declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    const expected = process.env.BADASS_ADMIN_PASSWORD;
    return expected && value === expected ? "ADMIN" : "DENIED";
}
process.stdout.write(run(process.argv[2]));
