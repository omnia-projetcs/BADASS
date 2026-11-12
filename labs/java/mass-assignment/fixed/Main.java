// Java profile binder allowlisting only the editable name field.
public class Main {
    static String run(String raw) {
        if (raw == null || raw.isEmpty()) return "DENIED";
        String name = "Alice";
        for (String pair : raw.split("&")) {
            String[] kv = pair.split("=", 2);
            if (kv.length == 2 && "name".equals(kv[0]) && kv[1].matches("[A-Za-z0-9_-]{1,32}")) {
                name = kv[1];
            }
        }
        return name + ":user";
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
