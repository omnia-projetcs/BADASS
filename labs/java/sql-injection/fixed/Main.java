import java.sql.*;

public class Main {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Expected one value");
        Class.forName("org.sqlite.JDBC");
        try (Connection db = DriverManager.getConnection("jdbc:sqlite::memory:")) {
            try (Statement setup = db.createStatement()) {
                setup.executeUpdate("CREATE TABLE users(name TEXT NOT NULL)");
                setup.executeUpdate("INSERT INTO users VALUES ('alice'),('admin')");
            }
            try (PreparedStatement query = db.prepareStatement("SELECT name FROM users WHERE name = ?")) {
                query.setString(1, args[0]);
                try (ResultSet rows = query.executeQuery()) {
                    while (rows.next()) System.out.println(rows.getString(1));
                }
            }
        }
    }
}
