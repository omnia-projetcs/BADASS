<?php
function run(string $value): string {
    if ($value === "ok") return "OK";
    $file = @fopen("missing-database", "r");
    if ($file === false) return "db://admin:LAB_SECRET@database/internal";
    fclose($file);
    return "OK";
}
echo run($argv[1]);
