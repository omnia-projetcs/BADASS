<?php
// PHP URL proxy handler enforcing HTTPS and an explicit host and path allowlist.
function run(string $rawUrl): string {
    $parts = parse_url($rawUrl);
    if (!is_array($parts)) return "DENIED";
    if (($parts["scheme"] ?? "") !== "https" || ($parts["host"] ?? "") !== "api.example.test"
        || isset($parts["port"]) || isset($parts["user"]) || ($parts["path"] ?? "") !== "/v1/status") {
        return "DENIED";
    }
    return "PUBLIC_OK";
}
echo run($argv[1]);
