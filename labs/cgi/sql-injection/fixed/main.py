import json
import os
from urllib.parse import parse_qs
import sqlite3
from contextlib import closing


def lookup(value):
    with closing(sqlite3.connect(':memory:')) as db:
        db.executescript("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');")
        return [row[0] for row in db.execute('SELECT name FROM users WHERE name = ?', (value,))]


def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get('name', [''])[0]
    return 'Content-Type: application/json\r\n\r\n' + json.dumps(lookup(value))


if __name__ == '__main__':
    print(run(os.environ.get('QUERY_STRING', '')), end='')
