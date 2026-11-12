// TypeScript profile update binding only the allowlisted display name field.
function updateProfile(raw: string): string {
    let incoming: unknown;
    try {
        incoming = JSON.parse(raw);
    } catch {
        return "DENIED";
    }
    if (incoming === null || typeof incoming !== "object" || Array.isArray(incoming)) {
        return "DENIED";
    }
    const record = incoming as Record<string, unknown>;
    const account = { name: "Alice", role: "user" };
    if (typeof record.name === "string" && /^[A-Za-z0-9 _-]{1,32}$/.test(record.name)) {
        account.name = record.name;
    }
    return `${account.name}:${account.role}`;
}
process.stdout.write(updateProfile(process.argv[2]));
