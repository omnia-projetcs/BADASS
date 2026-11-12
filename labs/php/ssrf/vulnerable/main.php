<?php
// PHP URL proxy handler allowing requests to link-local metadata and loopback addresses.
function run(string $rawUrl): string {
    $parts = parse_url($rawUrl);
    $host = $parts["host"] ?? "";
    if ($host === "169.254.169.254" || $host === "127.0.0.1") {
        return "LAB_INTERNAL_METADATA";
    }
    if (($parts["scheme"] ?? "") === "https" && $host === "api.example.test" && ($parts["path"] ?? "") === "/v1/status") {
        return "PUBLIC_OK";
    }
    return "NOT_FOUND";
}
echo run($argv[1]);
