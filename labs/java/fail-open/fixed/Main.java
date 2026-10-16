import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        try {
            if (value.equals("backend-down")) throw new IOException("Authorization unavailable");
            return value.equals("authorized") ? "ALLOWED" : "DENIED";
        } catch (IOException error) { return "DENIED"; }
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
