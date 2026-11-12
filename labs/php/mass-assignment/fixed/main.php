<?php
// PHP profile update allowlisting only the editable name attribute.
function run(string $raw): string {
    $account = ["name" => "Alice", "role" => "user"];
    $incoming = json_decode($raw, true);
    if (!is_array($incoming)) return "DENIED";
    if (isset($incoming["name"]) && is_string($incoming["name"]) && preg_match('/^[A-Za-z0-9 _-]{1,32}$/', $incoming["name"])) {
        $account["name"] = $incoming["name"];
    }
    return $account["name"] . ":" . $account["role"];
}
echo run($argv[1]);
