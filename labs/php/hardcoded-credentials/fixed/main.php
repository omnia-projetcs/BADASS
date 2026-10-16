<?php
function run(string $value): string {
    $expected = getenv("BADASS_ADMIN_PASSWORD");
    return $expected !== false && $expected !== "" && hash_equals($expected, $value) ? "ADMIN" : "DENIED";
}
echo run($argv[1]);
