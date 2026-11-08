<?php
function run(string $value): string {
    umask(0077);
    $file = fopen("stored-secret", "x");
    if (!$file) throw new RuntimeException("Creation failed");
    fwrite($file, $value === "public" ? "PUBLIC" : "LAB_SECRET");
    fclose($file);
    chmod("stored-secret", 0644);
    clearstatcache(true, "stored-secret");
    return sprintf("%04o", fileperms("stored-secret") & 0777);
}
echo run($argv[1]);
