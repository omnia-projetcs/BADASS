<?php
function run(string $value): string {
    if (!preg_match('/^[0-9]+$/', $value)) return "DENIED";
    $size = filter_var($value, FILTER_VALIDATE_INT);
    if ($size === false || $size < 0 || $size > 100) return "DENIED";
    $data = array_fill(0, $size, 0);
    return (string)count($data);
}
echo run($argv[1]);
