declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    if (!["/home", "/profile"].includes(value)) return "DENIED";
    return "Location: " + value;
}
process.stdout.write(run(process.argv[2]));
