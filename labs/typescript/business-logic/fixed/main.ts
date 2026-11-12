declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    if (typeof value !== "string" || !/^[0-9]+$/.test(value)) return "DENIED";
    const quantity = Number(value);
    if (!Number.isSafeInteger(quantity) || quantity < 1 || quantity > 100) return "DENIED";
    return String(1000 - quantity * 10);
}
process.stdout.write(run(process.argv[2]));
