function run(value) {
    const size = Number(value);
    if (!Number.isSafeInteger(size) || size < 0) throw new Error("Invalid size");
    if (size > 100) return "DENIED";
    const data = new Uint8Array(size);
    return String(data.length);
}
process.stdout.write(run(process.argv[2]));
