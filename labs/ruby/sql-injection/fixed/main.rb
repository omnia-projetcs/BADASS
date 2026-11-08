require 'sqlite3'

db = SQLite3::Database.new(':memory:')
begin
  db.execute_batch("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');")
  value = ARGV.fetch(0)
  rows = db.execute('SELECT name FROM users WHERE name = ?', [value])
  rows.each { |row| puts row[0] }
ensure
  db.close
end
