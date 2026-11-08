#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    sqlite3 *db = NULL;
    sqlite3_stmt *statement = NULL;
    int result = EXIT_FAILURE;
    if (argc != 2) return EXIT_FAILURE;
    if (sqlite3_open(":memory:", &db) != SQLITE_OK) goto cleanup;
    if (sqlite3_exec(db, "CREATE TABLE users(name TEXT NOT NULL);"
                        "INSERT INTO users VALUES ('alice'),('admin');",
                     NULL, NULL, NULL) != SQLITE_OK) goto cleanup;

    /* Preparing SQL alone is insufficient; bind the value separately. */
    if (sqlite3_prepare_v2(db, "SELECT name FROM users WHERE name = ?", -1,
                          &statement, NULL) != SQLITE_OK) goto cleanup;
    if (sqlite3_bind_text(statement, 1, argv[1], -1, SQLITE_TRANSIENT) != SQLITE_OK)
        goto cleanup;

    int status;
    while ((status = sqlite3_step(statement)) == SQLITE_ROW) {
        const unsigned char *name = sqlite3_column_text(statement, 0);
        if (!name) goto cleanup;
        puts((const char *)name);
    }
    if (status == SQLITE_DONE) result = EXIT_SUCCESS;
cleanup:
    if (result != EXIT_SUCCESS) fputs("SQLite operation failed\n", stderr);
    sqlite3_finalize(statement);
    if (db) sqlite3_close(db);
    return result;
}
