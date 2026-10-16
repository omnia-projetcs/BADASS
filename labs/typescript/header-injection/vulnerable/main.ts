declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    return 'X-User: ' + value + '\r\n\r\nBODY';
}
process.stdout.write(run(process.argv[2]));
