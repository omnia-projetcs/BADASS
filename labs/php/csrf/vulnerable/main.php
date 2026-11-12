<?php
// PHP transfer handler executing state-changing requests without verifying the anti-CSRF token.
function run(string $raw): string {
    $req = json_decode($raw, true);
    if (!is_array($req)) return "DENIED";
    return "TRANSFERRED";
}
echo run($argv[1]);
