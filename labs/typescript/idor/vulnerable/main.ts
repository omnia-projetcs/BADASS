declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    const records: Record<string, string> = {alice: "ALICE_DATA", bob: "BOB_PRIVATE"};
    if (!Object.prototype.hasOwnProperty.call(records, value)) return "NOT_FOUND";
    return records[value];
}
process.stdout.write(run(process.argv[2]));
