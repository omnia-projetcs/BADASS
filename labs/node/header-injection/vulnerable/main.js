function run(value) {
    return 'X-User: ' + value + '\r\n\r\nBODY';
}
process.stdout.write(run(process.argv[2]));
