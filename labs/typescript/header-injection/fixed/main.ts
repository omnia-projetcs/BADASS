declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    if (/[\r\n]/.test(value)) return 'DENIED';
    return 'X-User: ' + value + '\r\n\r\nBODY';
}
process.stdout.write(run(process.argv[2]));
