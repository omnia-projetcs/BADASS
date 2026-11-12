public class Main {
    static String run(String value) {
        if (value == null || !value.matches("[0-9]+")) return "DENIED";
        final int quantity;
        try {
            quantity = Integer.parseInt(value);
        } catch (NumberFormatException error) {
            return "DENIED";
        }
        if (quantity < 1 || quantity > 100) return "DENIED";
        return Integer.toString(1000 - quantity * 10);
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
