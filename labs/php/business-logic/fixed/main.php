<?php
function run(string $value): string {
    $quantity = filter_var($value, FILTER_VALIDATE_INT);
    if ($quantity === false) throw new RuntimeException("Invalid quantity");
    if ($quantity < 1 || $quantity > 100) return "DENIED";
    return (string)(1000 - $quantity * 10);
}
echo run($argv[1]);
