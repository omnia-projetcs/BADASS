import sqlite3
def run(value):
    with sqlite3.connect(':memory:') as db:
        db.executescript("CREATE TABLE users(name TEXT); INSERT INTO users VALUES ('alice'),('admin');")
        return [r[0] for r in db.execute("SELECT name FROM users WHERE name = '" + value + "'")]
