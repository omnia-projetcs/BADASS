using Microsoft.Data.Sqlite;

if (args.Length != 1) throw new ArgumentException("Expected one value");
using var db = new SqliteConnection("Data Source=:memory:");
db.Open();
using (var setup = db.CreateCommand())
{
    setup.CommandText = "CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');";
    setup.ExecuteNonQuery();
}
using var query = db.CreateCommand();
query.CommandText = "SELECT name FROM users WHERE name = $name";
query.Parameters.AddWithValue("$name", args[0]);
using var rows = query.ExecuteReader();
while (rows.Read()) Console.WriteLine(rows.GetString(0));
