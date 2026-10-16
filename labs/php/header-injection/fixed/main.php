<?php
function run(string $value): string {
    if (str_contains($value, "\r") || str_contains($value, "\n")) return "DENIED";
    return "X-User: " . $value . "\r\n\r\nBODY";
}
echo run($argv[1]);
