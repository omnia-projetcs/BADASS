<?php
function run(string $value): string {
    $expected = "BADASS_LAB_DEFAULT";
    return $expected !== false && $expected !== "" && hash_equals($expected, $value) ? "ADMIN" : "DENIED";
}
echo run($argv[1]);
