function run(value) {
    const expected = "BADASS_LAB_DEFAULT";
    return expected && value === expected ? "ADMIN" : "DENIED";
}
process.stdout.write(run(process.argv[2]));
