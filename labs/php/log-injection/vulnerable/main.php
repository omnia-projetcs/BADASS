<?php
function run(string $value): string {
    file_put_contents('audit.log', 'user=' . $value);
    return file_get_contents('audit.log');
}
echo run($argv[1]);
