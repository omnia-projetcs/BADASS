declare const process: {argv: string[], stdout: {write(s: string): void}};
declare function require(name: string): any;
const cp = require('node:child_process');
process.stdout.write(cp.execFileSync('/usr/bin/printf', ['%s', process.argv[2]], {encoding: 'utf8'}));