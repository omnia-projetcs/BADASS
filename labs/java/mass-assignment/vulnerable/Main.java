// Java profile binder applying all key=value pairs from request input including role.
public class Main {
    static String run(String raw) {
        String name = "Alice";
        String role = "user";
        for (String pair : raw.split("&")) {
            String[] kv = pair.split("=", 2);
            if (kv.length == 2) {
                if ("name".equals(kv[0])) name = kv[1];
                if ("role".equals(kv[0])) role = kv[1];
            }
        }
        return name + ":" + role;
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
