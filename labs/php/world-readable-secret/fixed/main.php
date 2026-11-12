<?php
function run(string $value): string {
    $previous = umask($value === "public" ? 0022 : 0077);
    try {
        $file = fopen("stored-secret", "x");
        if (!$file) throw new RuntimeException("Creation failed");
        try {
            fwrite($file, $value === "public" ? "PUBLIC" : "LAB_SECRET");
            fflush($file);
            $stat = fstat($file);
            return sprintf("%04o", $stat["mode"] & 0777);
        } finally {
            fclose($file);
        }
    } finally {
        umask($previous);
    }
}
echo run($argv[1]);
