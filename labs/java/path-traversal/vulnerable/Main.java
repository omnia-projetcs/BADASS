import java.nio.file.*;
import java.nio.charset.StandardCharsets;
public class Main { public static void main(String[] args) throws Exception {
System.out.print(Files.readString(Path.of("public", args[0])));
}}
