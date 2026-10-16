<?php
function run(string $value): string {
    $value = str_replace(["\\", "\r", "\n"], ["\\\\", "\\r", "\\n"], $value);
    file_put_contents('audit.log', 'user=' . $value);
    return file_get_contents('audit.log');
}
echo run($argv[1]);
