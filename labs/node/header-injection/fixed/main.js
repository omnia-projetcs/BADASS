function run(value) {
    if (/[\r\n]/.test(value)) return 'DENIED';
    return 'X-User: ' + value + '\r\n\r\nBODY';
}
process.stdout.write(run(process.argv[2]));
