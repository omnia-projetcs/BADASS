function run(value) {
    if (typeof value !== "string" || !/^[0-9]+$/.test(value)) return "DENIED";
    const size = Number(value);
    if (!Number.isSafeInteger(size) || size < 0 || size > 100) return "DENIED";
    const data = new Uint8Array(size);
    return String(data.length);
}
process.stdout.write(run(process.argv[2]));
