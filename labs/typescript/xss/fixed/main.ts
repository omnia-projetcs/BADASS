declare const process: {argv: string[], stdout: {write(s: string): void}};
declare function require(name: string): any;
const value = process.argv[2].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
process.stdout.write('<p>' + value + '</p>');