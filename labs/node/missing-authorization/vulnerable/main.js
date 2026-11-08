function run(value) {
    if (value === "health") return "HEALTHY";
    const session = {role: "user"};
    const users = ["alice", "bob"];
    users.length = 0;
    return "USERS_DELETED";
}
process.stdout.write(run(process.argv[2]));
