// Java URI fetcher enforcing HTTPS and a strict host and path allowlist.
import java.net.URI;

public class Main {
    static String run(String rawUrl) {
        try {
            URI uri = new URI(rawUrl);
            if (!"https".equals(uri.getScheme()) || !"api.example.test".equals(uri.getHost())
                || uri.getPort() != -1 || !"/v1/status".equals(uri.getPath()) || uri.getUserInfo() != null) {
                return "DENIED";
            }
            return "PUBLIC_OK";
        } catch (Exception ex) {
            return "DENIED";
        }
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
