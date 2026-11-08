<?php
function run(string $value): string {
    $records = ["alice" => "ALICE_DATA", "bob" => "BOB_PRIVATE"];
    if (!array_key_exists($value, $records)) return "NOT_FOUND";
    if ($value !== "alice") return "DENIED";
    return $records[$value];
}
echo run($argv[1]);
