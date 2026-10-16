declare const process: {argv: string[], stdout: {write(s: string): void}};
declare function require(name: string): any;
const fs = require('node:fs');
process.stdout.write(fs.readFileSync('public/' + process.argv[2], 'utf8'));