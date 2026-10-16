declare const process: {argv: string[], stdout: {write(s: string): void}};
declare function require(name: string): any;
const incoming = JSON.parse(process.argv[2]);
const target: any = {};
Object.assign(target, incoming);
process.stdout.write(target.isAdmin === true ? 'ADMIN' : 'USER');