function run(value) {
    return "Location: " + value;
}
process.stdout.write(run(process.argv[2]));
