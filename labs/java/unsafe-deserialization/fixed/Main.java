// Java deserialization handler rejecting class-descriptor payloads and enforcing safe JSON strings.
public class Main {
    static String run(String payload) {
        if (payload == null || !payload.startsWith("JSON:")) {
            return "DENIED";
        }
        String value = payload.substring(5);
        if (!value.matches("[A-Za-z0-9_-]{1,32}")) {
            return "DENIED";
        }
        return value;
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
