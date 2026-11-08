"""Query a small database through a role-aware gateway."""
import sqlite3

USERS = {"LAB_ADMIN": "admin", "LAB_READER": "reader"}


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("token"), str) or request["token"] not in USERS:
        return {"status": 401, "error": "denied"}
    table, order, name = request.get("table"), request.get("order_by"), request.get("name")
    if not isinstance(table, str) or table not in {"documents", "roles"} or (order is not None and (not isinstance(order, str) or order not in {"name", "name DESC"})) or (name is not None and (not isinstance(name, str) or len(name) > 128)):
        return {"status": 400, "error": "invalid query"}
    role = USERS[request["token"]]
    if table == "roles" and role != "admin":
        return {"status": 403, "error": "restricted table"}
    db = sqlite3.connect(":memory:")
    try:
        db.executescript("CREATE TABLE documents(name TEXT); INSERT INTO documents VALUES('public');"
                         "CREATE TABLE roles(name TEXT); INSERT INTO roles VALUES('admin'), ('reader');")
        sql, values = "SELECT name FROM " + table, ()
        if name is not None:
            sql += " WHERE name = ?"
            values = (name,)
        if order is not None:
            sql += " ORDER BY " + order
        return {"status": 200, "rows": [row[0] for row in db.execute(sql, values)]}
    finally:
        db.close()
