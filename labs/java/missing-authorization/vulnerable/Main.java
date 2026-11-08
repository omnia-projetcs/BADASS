import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.io.IOException;

public class Main {
    static String run(String value) throws Exception {
        if (value.equals("health")) return "HEALTHY";
        String role = "user";
        List<String> users = new ArrayList<>(List.of("alice", "bob"));
        users.clear();
        return "USERS_DELETED";
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
