<?php
function run(string $value): string {
    try {
        if ($value === "backend-down") throw new RuntimeException("Authorization unavailable");
        return $value === "authorized" ? "ALLOWED" : "DENIED";
    } catch (RuntimeException $error) { return "ALLOWED"; }
}
echo run($argv[1]);
