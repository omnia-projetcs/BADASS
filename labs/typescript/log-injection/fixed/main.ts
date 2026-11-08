declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    value = value.replace(/\\/g, '\\\\').replace(/\r/g, '\\r').replace(/\n/g, '\\n');
    const fs = require('node:fs');
    fs.writeFileSync('audit.log', 'user=' + value);
    return fs.readFileSync('audit.log', 'utf8');
}
process.stdout.write(run(process.argv[2]));
