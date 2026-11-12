<?php
// PHP session loader using json_decode() and rejecting PHP object serialization formats.
function run(string $raw): string {
    if (str_starts_with($raw, "O:") || str_starts_with($raw, "C:")) {
        return "DENIED";
    }
    $data = json_decode($raw, true);
    if (!is_array($data) || !isset($data["user"]) || !is_string($data["user"])) {
        return "DENIED";
    }
    if (!preg_match('/^[a-z0-9_]{1,32}$/', $data["user"])) {
        return "DENIED";
    }
    return "USER:" . $data["user"];
}
echo run($argv[1]);
