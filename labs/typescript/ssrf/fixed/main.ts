// TypeScript webhook dispatcher enforcing HTTPS and an allowlisted upstream host.
function dispatchWebhook(rawUrl: string): string {
    let parsed: URL;
    try {
        parsed = new URL(rawUrl);
    } catch {
        return "DENIED";
    }
    if (parsed.protocol !== "https:" || parsed.hostname !== "api.example.test" || parsed.port !== "" || parsed.pathname !== "/v1/status" || parsed.username !== "") {
        return "DENIED";
    }
    return "PUBLIC_OK";
}
process.stdout.write(dispatchWebhook(process.argv[2]));
