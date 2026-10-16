<?php
function run(string $value): string {
    if (!in_array($value, ["/home", "/profile"], true)) return "DENIED";
    return "Location: " . $value;
}
echo run($argv[1]);
