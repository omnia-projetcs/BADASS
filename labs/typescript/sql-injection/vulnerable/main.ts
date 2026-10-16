declare const process: {argv: string[], stdout: {write(s: string): void}, stderr: {write(s: string): void}, exitCode: number};
declare function require(name: string): any;

const sqlite3 = require('sqlite3');
const db = new sqlite3.Database(':memory:');
const value = process.argv[2];

function finish(error: Error | null, rows: {name: string}[]): void {
    if (error) {
        process.stderr.write(String(error));
        process.exitCode = 1;
    } else {
        process.stdout.write(rows.map((row: {name: string}) => row.name).join('\n'));
    }
    db.close((closeError: Error | null) => {
        if (closeError) {
            process.stderr.write(String(closeError));
            process.exitCode = 1;
        }
    });
}

db.exec("CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');", (error: Error | null) => {
    if (error) { finish(error, []); return; }
    db.all("SELECT name FROM users WHERE name = '" + value + "'", [], finish);
});
