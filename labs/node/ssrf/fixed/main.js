// Node.js URL preview handler enforcing HTTPS and an exact origin and path allowlist.
function run(rawUrl) {
    let parsed;
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
process.stdout.write(run(process.argv[2]));
