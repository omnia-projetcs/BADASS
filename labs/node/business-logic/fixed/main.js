function run(value) {
    const quantity = Number(value);
    if (!Number.isSafeInteger(quantity)) throw new Error("Invalid quantity");
    if (quantity < 1 || quantity > 100) return "DENIED";
    return String(1000 - quantity * 10);
}
process.stdout.write(run(process.argv[2]));
