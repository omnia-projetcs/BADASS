import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class Main {
    static String run(String value) {
        String expected = System.getenv("BADASS_ADMIN_PASSWORD");
        if (expected == null || expected.isEmpty() || value == null) {
            return "DENIED";
        }
        boolean matches = MessageDigest.isEqual(
            expected.getBytes(StandardCharsets.UTF_8),
            value.getBytes(StandardCharsets.UTF_8)
        );
        return matches ? "ADMIN" : "DENIED";
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
