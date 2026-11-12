// TypeScript webhook dispatcher allowing internal metadata and loopback URLs.
function dispatchWebhook(rawUrl: string): string {
    const parsed = new URL(rawUrl);
    if (parsed.hostname === "169.254.169.254" || parsed.hostname === "127.0.0.1") {
        return "LAB_INTERNAL_METADATA";
    }
    if (parsed.protocol === "https:" && parsed.hostname === "api.example.test" && parsed.pathname === "/v1/status") {
        return "PUBLIC_OK";
    }
    return "NOT_FOUND";
}
process.stdout.write(dispatchWebhook(process.argv[2]));
