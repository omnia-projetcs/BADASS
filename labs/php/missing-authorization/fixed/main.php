<?php
function run(string $value): string {
    if ($value === "health") return "HEALTHY";
    $role = "user";
    $users = ["alice", "bob"];
    if ($role !== "admin") return "DENIED";
    $users = [];
    return "USERS_DELETED";
}
echo run($argv[1]);
