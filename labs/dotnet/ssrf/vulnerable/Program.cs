// .NET Uri fetcher permitting link-local metadata and loopback destinations.
Console.Write(Run(args[0]));

static string Run(string rawUrl) {
    var uri = new Uri(rawUrl);
    if (uri.Host == "169.254.169.254" || uri.Host == "127.0.0.1") {
        return "LAB_INTERNAL_METADATA";
    }
    if (uri.Scheme == "https" && uri.Host == "api.example.test" && uri.AbsolutePath == "/v1/status") {
        return "PUBLIC_OK";
    }
    return "NOT_FOUND";
}
