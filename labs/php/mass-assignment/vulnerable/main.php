<?php
// PHP profile update merging all decoded JSON keys into the user record.
function run(string $raw): string {
    $account = ["name" => "Alice", "role" => "user"];
    $incoming = json_decode($raw, true);
    if (is_array($incoming)) {
        $account = array_merge($account, $incoming);
    }
    return $account["name"] . ":" . $account["role"];
}
echo run($argv[1]);
