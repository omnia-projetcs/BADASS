// Node.js profile update handler allowlisting only the editable name property.
function run(raw) {
    let incoming;
    try {
        incoming = JSON.parse(raw);
    } catch {
        return "DENIED";
    }
    if (incoming === null || typeof incoming !== "object" || Array.isArray(incoming)) {
        return "DENIED";
    }
    const account = { name: "Alice", role: "user" };
    if (typeof incoming.name === "string" && /^[A-Za-z0-9 _-]{1,32}$/.test(incoming.name)) {
        account.name = incoming.name;
    }
    return `${account.name}:${account.role}`;
}
process.stdout.write(run(process.argv[2]));
