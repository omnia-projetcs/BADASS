// .NET Uri fetcher enforcing HTTPS and an allowlisted upstream host and path.
Console.Write(Run(args[0]));

static string Run(string rawUrl) {
    if (!Uri.TryCreate(rawUrl, UriKind.Absolute, out var uri)) return "DENIED";
    if (uri.Scheme != Uri.UriSchemeHttps || uri.Host != "api.example.test" || !uri.IsDefaultPort || uri.AbsolutePath != "/v1/status" || !string.IsNullOrEmpty(uri.UserInfo)) {
        return "DENIED";
    }
    return "PUBLIC_OK";
}
