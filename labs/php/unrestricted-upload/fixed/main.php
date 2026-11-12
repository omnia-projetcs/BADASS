<?php
// PHP upload handler enforcing a strict basename and .txt/.png extension allowlist.
function run(string $filename): string {
    if (!preg_match('/^[A-Za-z0-9_-]{1,32}\.(txt|png)$/', $filename)) {
        return "DENIED";
    }
    return "SAVED:" . $filename;
}
echo run($argv[1]);
