// Java deserialization handler instantiating caller-specified class names before validation.
public class Main {
    static String run(String payload) {
        if (payload.startsWith("CLASS:ExecGadget:")) {
            return "LAB_GADGET_EXECUTED";
        }
        if (payload.startsWith("JSON:")) {
            return payload.substring(5);
        }
        return "DENIED";
    }
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
