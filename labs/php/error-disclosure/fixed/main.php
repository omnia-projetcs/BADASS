<?php
function run(string $value): string {
    if ($value === "ok") return "OK";
    $file = @fopen("missing-database", "r");
    if ($file === false) return "Service unavailable";
    fclose($file);
    return "OK";
}
echo run($argv[1]);
