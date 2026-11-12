// TypeScript profile update spreading untrusted JSON fields over an account record.
function updateProfile(raw: string): string {
    const base = { name: "Alice", role: "user" };
    const updated = { ...base, ...JSON.parse(raw) };
    return `${updated.name}:${updated.role}`;
}
process.stdout.write(updateProfile(process.argv[2]));
