declare const process: {argv: string[], env: {[key: string]: string | undefined}, stdout: {write(s: string): void}};
declare function require(name: string): any;
function run(value: string): string {
    if (value === "health") return "HEALTHY";
    const session = {role: "user"};
    const users = ["alice", "bob"];
    if (session.role !== "admin") return "DENIED";
    users.length = 0;
    return "USERS_DELETED";
}
process.stdout.write(run(process.argv[2]));
