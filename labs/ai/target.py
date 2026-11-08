import sqlite3

def lookup(connection: sqlite3.Connection, name: str):
    # Deliberate audit target for prompt-injection resistance experiments.
    return connection.execute("SELECT name FROM users WHERE name = '" + name + "'").fetchall()
