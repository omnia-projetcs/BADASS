declare const process: {argv: string[], stdout: {write(s: string): void}};
declare function require(name: string): any;
process.stdout.write('<p>' + process.argv[2] + '</p>');