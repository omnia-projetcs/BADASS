<?php
function run(string $value): string {
    if ($value === "preplaced-link") symlink("secret.txt", "export.tmp");
    $file = @fopen("export.tmp", "x");
    if ($file !== false) { fwrite($file, "LAB_OVERWRITTEN"); fclose($file); }
    elseif (!is_link("export.tmp") && !file_exists("export.tmp")) throw new RuntimeException("Export failed");
    return file_get_contents("secret.txt");
}
echo run($argv[1]);
