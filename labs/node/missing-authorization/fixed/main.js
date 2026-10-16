function run(value) {
    if (value === "health") return "HEALTHY";
    const session = {role: "user"};
    const users = ["alice", "bob"];
    if (session.role !== "admin") return "DENIED";
    users.length = 0;
    return "USERS_DELETED";
}
process.stdout.write(run(process.argv[2]));
