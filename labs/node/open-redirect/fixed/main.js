function run(value) {
    if (!["/home", "/profile"].includes(value)) return "DENIED";
    return "Location: " + value;
}
process.stdout.write(run(process.argv[2]));
