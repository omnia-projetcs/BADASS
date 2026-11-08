<?php
function run(string $value): string {
    return "X-User: " . $value . "\r\n\r\nBODY";
}
echo run($argv[1]);
