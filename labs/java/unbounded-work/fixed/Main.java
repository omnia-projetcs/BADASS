public class Main {
    static String run(String value) {
        if (value == null || !value.matches("[0-9]+")) return "DENIED";
        final int size;
        try {
            size = Integer.parseInt(value);
        } catch (NumberFormatException error) {
            return "DENIED";
        }
        if (size < 0 || size > 100) return "DENIED";
        byte[] data = new byte[size];
        return Integer.toString(data.length);
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
