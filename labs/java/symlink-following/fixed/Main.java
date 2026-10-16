import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        if (value.equals("preplaced-link")) Files.createSymbolicLink(Path.of("export.tmp"), Path.of("secret.txt"));
        try {
            Files.writeString(Path.of("export.tmp"), "LAB_OVERWRITTEN", StandardOpenOption.WRITE, StandardOpenOption.CREATE_NEW);
        } catch (FileAlreadyExistsException error) {
            // Existing paths are rejected without following the link.
        }
        return Files.readString(Path.of("secret.txt"));
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
