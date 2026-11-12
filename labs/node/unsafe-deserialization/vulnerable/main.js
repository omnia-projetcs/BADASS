// Node.js deserializer evaluating _$$ND_FUNC$$_ IIFE markers in untrusted JSON.
function run(raw) {
    const obj = JSON.parse(raw);
    if (typeof obj.value === "string" && obj.value.startsWith("_$$ND_FUNC$$_")) {
        return "LAB_NODE_EXEC";
    }
    return "VALUE:" + String(obj.value);
}
process.stdout.write(run(process.argv[2]));
