function run(value) {
    const records = {alice: "ALICE_DATA", bob: "BOB_PRIVATE"};
    if (!Object.prototype.hasOwnProperty.call(records, value)) return "NOT_FOUND";
    if (value !== "alice") return "DENIED";
    return records[value];
}
process.stdout.write(run(process.argv[2]));
