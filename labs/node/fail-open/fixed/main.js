function run(value) {
    try {
        if (value === "backend-down") throw new Error("Authorization unavailable");
        return value === "authorized" ? "ALLOWED" : "DENIED";
    } catch (error) { return "DENIED"; }
}
process.stdout.write(run(process.argv[2]));
