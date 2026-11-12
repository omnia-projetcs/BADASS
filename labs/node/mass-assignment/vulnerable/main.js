// Node.js profile update handler copying all incoming properties onto the account model.
function run(raw) {
    const account = { name: "Alice", role: "user" };
    Object.assign(account, JSON.parse(raw));
    return `${account.name}:${account.role}`;
}
process.stdout.write(run(process.argv[2]));
