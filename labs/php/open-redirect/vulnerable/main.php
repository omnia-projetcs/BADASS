<?php
function run(string $value): string {
    return "Location: " . $value;
}
echo run($argv[1]);
