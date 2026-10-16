import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        Files.writeString(Path.of("audit.log"), "user=" + value);
        return Files.readString(Path.of("audit.log"));
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
