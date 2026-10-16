function run(value) {
    const quantity = Number(value);
    if (!Number.isSafeInteger(quantity)) throw new Error("Invalid quantity");
    return String(1000 - quantity * 10);
}
process.stdout.write(run(process.argv[2]));
