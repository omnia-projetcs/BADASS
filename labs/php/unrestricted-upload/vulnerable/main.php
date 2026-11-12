<?php
// PHP upload handler accepting executable .php filenames without extension allowlisting.
function run(string $filename): string {
    if ($filename === "" || str_contains($filename, "/") || str_contains($filename, "\\")) {
        return "DENIED";
    }
    return "SAVED:" . $filename;
}
echo run($argv[1]);
