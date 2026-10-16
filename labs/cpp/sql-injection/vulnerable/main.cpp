#include <sqlite3.h>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

void require_ok(int status) {
    if (status != SQLITE_OK) throw std::runtime_error("SQLite operation failed");
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    try {
        sqlite3 *raw_db = nullptr;
        int status = sqlite3_open(":memory:", &raw_db);
        std::unique_ptr<sqlite3, decltype(&sqlite3_close)> db(raw_db, sqlite3_close);
        require_ok(status);
        require_ok(sqlite3_exec(db.get(), "CREATE TABLE users(name TEXT NOT NULL);"
                                         "INSERT INTO users VALUES ('alice'),('admin');",
                                nullptr, nullptr, nullptr));
        std::string value = argv[1];
        std::string query = "SELECT name FROM users WHERE name = '" + value + "'";
        sqlite3_stmt *raw_statement = nullptr;
        status = sqlite3_prepare_v2(db.get(), query.c_str(), -1, &raw_statement, nullptr);
        std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> statement(raw_statement, sqlite3_finalize);
        require_ok(status);
        while ((status = sqlite3_step(statement.get())) == SQLITE_ROW) {
            const auto *name = sqlite3_column_text(statement.get(), 0);
            if (!name) throw std::runtime_error("Unexpected NULL result");
            std::cout << name << '\n';
        }
        if (status != SQLITE_DONE) throw std::runtime_error("SQLite query failed");
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
