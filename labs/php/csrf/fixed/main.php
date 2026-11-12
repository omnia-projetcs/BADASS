<?php
// PHP transfer handler verifying the session anti-CSRF token with hash_equals().
function run(string $raw): string {
    $req = json_decode($raw, true);
    if (!is_array($req) || !isset($req["csrf"]) || !is_string($req["csrf"])) {
        return "DENIED";
    }
    if (!hash_equals("lab-session-csrf-token", $req["csrf"])) {
        return "DENIED";
    }
    return "TRANSFERRED";
}
echo run($argv[1]);
