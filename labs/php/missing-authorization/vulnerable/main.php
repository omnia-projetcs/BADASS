<?php
function run(string $value): string {
    if ($value === "health") return "HEALTHY";
    $role = "user";
    $users = ["alice", "bob"];
    $users = [];
    return "USERS_DELETED";
}
echo run($argv[1]);
