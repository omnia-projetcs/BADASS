// Node.js URL preview handler allowing requests to internal metadata and loopback hosts.
function run(rawUrl) {
    const parsed = new URL(rawUrl);
    if (parsed.hostname === "169.254.169.254" || parsed.hostname === "127.0.0.1") {
        return "LAB_INTERNAL_METADATA";
    }
    if (parsed.protocol === "https:" && parsed.hostname === "api.example.test" && parsed.pathname === "/v1/status") {
        return "PUBLIC_OK";
    }
    return "NOT_FOUND";
}
process.stdout.write(run(process.argv[2]));
