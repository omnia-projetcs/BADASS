<?php
function run(string $value): string {
    if (!preg_match('/^[0-9]+$/', $value)) return "DENIED";
    $quantity = filter_var($value, FILTER_VALIDATE_INT);
    if ($quantity === false || $quantity < 1 || $quantity > 100) return "DENIED";
    return (string)(1000 - $quantity * 10);
}
echo run($argv[1]);
