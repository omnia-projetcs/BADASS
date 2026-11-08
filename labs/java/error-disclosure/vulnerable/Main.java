import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        if (value.equals("ok")) return "OK";
        try { Files.readString(Path.of("missing-database")); }
        catch (NoSuchFileException error) { return "db://admin:LAB_SECRET@database/internal"; }
        return "OK";
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
