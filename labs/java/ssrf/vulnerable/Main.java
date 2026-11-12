// Java URI fetcher allowing requests to link-local metadata and loopback addresses.
import java.net.URI;

public class Main {
    static String run(String rawUrl) throws Exception {
        URI uri = new URI(rawUrl);
        String host = uri.getHost();
        if ("169.254.169.254".equals(host) || "127.0.0.1".equals(host)) {
            return "LAB_INTERNAL_METADATA";
        }
        if ("https".equals(uri.getScheme()) && "api.example.test".equals(host) && "/v1/status".equals(uri.getPath())) {
            return "PUBLIC_OK";
        }
        return "NOT_FOUND";
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
