<?php
function run(string $value): string {
    $size = filter_var($value, FILTER_VALIDATE_INT);
    if ($size === false || $size < 0) throw new RuntimeException("Invalid size");
    $data = array_fill(0, $size, 0);
    return (string)count($data);
}
echo run($argv[1]);
