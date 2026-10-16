import java.nio.file.*;
import java.nio.charset.StandardCharsets;
public class Main { public static void main(String[] args) throws Exception {
Process p = new ProcessBuilder("/bin/sh", "-c", "printf %s " + args[0]).start(); System.out.print(new String(p.getInputStream().readAllBytes(), StandardCharsets.UTF_8)); if(p.waitFor()!=0) throw new Exception("command failed");
}}
