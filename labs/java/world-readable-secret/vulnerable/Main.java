import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        Path path = Path.of("stored-secret");
        Files.createFile(path, PosixFilePermissions.asFileAttribute(PosixFilePermissions.fromString("rw-------")));
        Files.writeString(path, value.equals("public") ? "PUBLIC" : "LAB_SECRET");
        Files.setPosixFilePermissions(path, PosixFilePermissions.fromString("rw-r--r--"));
        int mode = (Integer) Files.getAttribute(path, "unix:mode");
        return String.format("%04o", mode & 0777);
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
