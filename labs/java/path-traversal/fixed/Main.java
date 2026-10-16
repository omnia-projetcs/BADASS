import java.nio.file.*;
import java.nio.charset.StandardCharsets;
public class Main { public static void main(String[] args) throws Exception {
System.out.print(args[0].equals("welcome.txt") ? Files.readString(Path.of("public/welcome.txt")) : "DENIED");
}}
