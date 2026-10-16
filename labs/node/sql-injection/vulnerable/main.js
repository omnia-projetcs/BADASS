const sqlite3 = require('sqlite3');
const db = new sqlite3.Database(':memory:');
const value = process.argv[2];

function finish(error, rows) {
    if (error) {
        process.stderr.write(String(error));
        process.exitCode = 1;
    } else {
        process.stdout.write(rows.map((row) => row.name).join('\n'));
    }
    db.close((closeError) => {
        if (closeError) {
            process.stderr.write(String(closeError));
            process.exitCode = 1;
        }
    });
}

db.exec("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');", (error) => {
    if (error) { finish(error, []); return; }
    db.all("SELECT name FROM users WHERE name = '" + value + "'", [], finish);
});
