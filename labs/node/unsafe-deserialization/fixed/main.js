// Node.js deserializer rejecting serialized function markers and enforcing plain string values.
function run(raw) {
    let obj;
    try {
        obj = JSON.parse(raw);
    } catch {
        return "DENIED";
    }
    if (obj === null || typeof obj !== "object" || Array.isArray(obj)) {
        return "DENIED";
    }
    if (typeof obj.value !== "string" || obj.value.includes("_$$ND_FUNC$$_") || !/^[a-zA-Z0-9_-]{1,32}$/.test(obj.value)) {
        return "DENIED";
    }
    return "VALUE:" + obj.value;
}
process.stdout.write(run(process.argv[2]));
