import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        Map<String, String> records = Map.of("alice", "ALICE_DATA", "bob", "BOB_PRIVATE");
        if (!records.containsKey(value)) return "NOT_FOUND";
        return records.get(value);
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
