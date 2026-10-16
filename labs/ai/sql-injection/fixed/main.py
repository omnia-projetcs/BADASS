import sqlite3
from contextlib import closing


def lookup(value):
    with closing(sqlite3.connect(':memory:')) as db:
        db.executescript("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');")
        return [row[0] for row in db.execute('SELECT name FROM users WHERE name = ?', (value,))]


def run(tool_arguments):
    # Treat model-supplied tool arguments as untrusted input.
    # The application owns the query shape; this fixture does not run an LLM.
    return lookup(tool_arguments['name'])
