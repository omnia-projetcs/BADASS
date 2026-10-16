function run(value) {
    const expected = process.env.BADASS_ADMIN_PASSWORD;
    return expected && value === expected ? "ADMIN" : "DENIED";
}
process.stdout.write(run(process.argv[2]));
