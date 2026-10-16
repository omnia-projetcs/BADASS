<?php
function run(string $value): string {
    $quantity = filter_var($value, FILTER_VALIDATE_INT);
    if ($quantity === false) throw new RuntimeException("Invalid quantity");
    return (string)(1000 - $quantity * 10);
}
echo run($argv[1]);
