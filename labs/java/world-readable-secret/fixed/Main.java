import java.nio.ByteBuffer;
import java.nio.channels.SeekableByteChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.EnumSet;

public class Main {
    static String run(String value) throws Exception {
        Path path = Path.of("stored-secret");
        String perms = "public".equals(value) ? "rw-r--r--" : "rw-------";
        byte[] content = ("public".equals(value) ? "PUBLIC" : "LAB_SECRET").getBytes(StandardCharsets.UTF_8);
        try (SeekableByteChannel channel = Files.newByteChannel(
                path,
                EnumSet.of(StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE),
                PosixFilePermissions.asFileAttribute(PosixFilePermissions.fromString(perms)))) {
            channel.write(ByteBuffer.wrap(content));
        }
        int mode = (Integer) Files.getAttribute(path, "unix:mode", LinkOption.NOFOLLOW_LINKS);
        return String.format("%04o", mode & 0777);
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one input");
        System.out.print(run(args[0]));
    }
}
