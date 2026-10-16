import sqlite3
from contextlib import closing


def lookup(value):
    with closing(sqlite3.connect(':memory:')) as db:
        db.executescript("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');")
        return [row[0] for row in db.execute("SELECT name FROM users WHERE name = '" + value + "'")]


def run(request):
    # The request object represents decoded JSON at the handler boundary.
    return {'status': 200, 'body': lookup(request['name'])}
