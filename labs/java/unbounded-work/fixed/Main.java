import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        int size = Integer.parseInt(value);
        if (size < 0) throw new IllegalArgumentException("Invalid size");
        if (size > 100) return "DENIED";
        byte[] data = new byte[size];
        return Integer.toString(data.length);
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
