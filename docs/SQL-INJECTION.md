# SQL injection across technologies

Every technology section contains a `sql-injection` pair mapped to **CWE-89** and
**OWASP A05:2025**. Each example creates a fresh SQLite database in memory, inserts
two synthetic accounts, executes an actual SELECT, and returns the retrieved rows.
The vulnerable variant concatenates a value into SQL. The corrected variant keeps
the statement structure constant and binds the value through the database API.

| Technology | Database interface | Corrected query binding | Case |
|---|---|---|---|
| C | SQLite C API | `sqlite3_prepare_v2` and `sqlite3_bind_text` | [Source pair](../labs/c/sql-injection/README.md) |
| C++ | SQLite C API with RAII handles | `sqlite3_prepare_v2` and `sqlite3_bind_text` | [Source pair](../labs/cpp/sql-injection/README.md) |
| Go | `database/sql`, `mattn/go-sqlite3` | `db.Query(sql, value)` | [Source pair](../labs/go/sql-injection/README.md) |
| PHP | PDO SQLite | `prepare` and `execute([$value])` | [Source pair](../labs/php/sql-injection/README.md) |
| Node.js | `sqlite3` | `db.all(sql, [value], callback)` | [Source pair](../labs/node/sql-injection/README.md) |
| TypeScript | `sqlite3` | `db.all(sql, [value], callback)` | [Source pair](../labs/typescript/sql-injection/README.md) |
| Python | Standard-library `sqlite3` | `execute(sql, (value,))` | [Source pair](../labs/python/sql-injection/README.md) |
| CGI | Python `sqlite3`, decoded `QUERY_STRING` | `execute(sql, (value,))` | [Source pair](../labs/cgi/sql-injection/README.md) |
| REST API | Python JSON handler and `sqlite3` | `execute(sql, (value,))` | [Source pair](../labs/rest-api/sql-injection/README.md) |
| .NET / C# | `Microsoft.Data.Sqlite` | `Parameters.AddWithValue` | [Source pair](../labs/dotnet/sql-injection/README.md) |
| Java | SQLite JDBC | `PreparedStatement.setString` | [Source pair](../labs/java/sql-injection/README.md) |
| Ruby | `sqlite3` gem | `execute(sql, [value])` | [Source pair](../labs/ruby/sql-injection/README.md) |
| Rust | Native SQLite API through FFI | `sqlite3_prepare_v2` and `sqlite3_bind_text` | [Source pair](../labs/rust/sql-injection/README.md) |
| AI / LLM boundary | Python database tool accepting model arguments | `execute(sql, (value,))` | [Source pair](../labs/ai/sql-injection/README.md) |

The AI case is also mapped to **LLM05:2025**: model-generated tool arguments are
untrusted database input. The application owns the SQL structure. No live model
is invoked and this test does not establish prompt-injection resistance.

## Regression vectors

All 14 pairs run the same seven logical vectors, adapted to their input/output
contract. The CGI case parses URL-encoded parameters and returns a CGI response;
the REST case receives a decoded JSON object and returns a handler response.

| Input | Purpose | Vulnerable result | Corrected result |
|---|---|---|---|
| `alice` | Existing account | `alice` | `alice` |
| `unknown` | Absent account | No rows | No rows |
| Empty string | Empty lookup | No rows | No rows |
| `UNION SELECT admin` | Ordinary SQL-looking value | No rows | No rows |
| `' OR 1=1 --` | Predicate bypass and comment | `alice`, `admin` | No rows |
| `' OR name='admin' --` | Targeted account bypass | `admin` | No rows |
| `' UNION SELECT 'LAB_UNION' --` | Injected result row | `LAB_UNION` | No rows |

This produces **196 assertions**: seven inputs × two variants × 14 technologies.
The full SQL engine processes the vulnerable expressions; no mock parser or
payload allowlist stands in for query execution.

These are focused SQLite examples, not an exhaustive SQL injection test suite.
PostgreSQL, MySQL, SQL Server, ORM query builders, dynamic identifiers, stored
procedures, second-order injection and timing channels require additional cases.
Preparing an already-concatenated SQL string does not prevent injection; the
corrected variants bind values separately from query syntax.

## Running the suite

Rebuild the image if it predates the SQLite cases:

```sh
make container-build
make container-test LAB_ARGS='test --cwe CWE-89 --strict --output reports/sql-injection.json'

# Run a single SQL case, or the entire corpus.
make container-test LAB_ARGS='test --case java/sql-injection --strict'
make container-test
```

The container installs dependencies during its build and runs with external
networking disabled. Database contents are created per process and are never
persisted to the source tree.

For a native Linux run, install the dependencies below in addition to the base
language toolchain, or use the supplied container:

| Technology | Additional dependency or runner configuration |
|---|---|
| C / C++ / Rust | `libsqlite3-dev`; C/C++ link with `-lsqlite3`, Rust declares a native link |
| Go | `golang-github-mattn-go-sqlite3-dev`; the runner enables CGO and uses the offline source tree under `/usr/share/gocode` with the `libsqlite3` build tag |
| PHP | `php-sqlite3` with PDO SQLite enabled |
| Node.js / TypeScript | `node-sqlite3`, resolvable by `require('sqlite3')` |
| Java | `libxerial-sqlite-jdbc-java`, including its native JNI dependency |
| Ruby | `ruby-sqlite3` |
| .NET | `Microsoft.Data.Sqlite` 8.0.21 and its transitive dependencies; preloaded in the image |
| Python / CGI / REST API / AI | Python's `sqlite3` standard-library module |

`BADASS_GO_SQLITE_GOPATH` can override the Go driver source tree.
`BADASS_SQLITE_JDBC_JAR` can override `/usr/share/java/sqlite-jdbc.jar`.
`BADASS_NUGET_PACKAGES` and `BADASS_NUGET_SOURCE` configure the preloaded NuGet
cache/feed; the image sets them to `/opt/nuget/packages` and `/opt/nuget/feed`.
A native .NET run without a preloaded cache may require a network restore first.
Missing drivers are reported as failures, never as passing regressions.

The Rust fixtures use a small native API binding to avoid downloading Cargo
dependencies. Opaque handles are released with `Drop`, result pointers are checked,
and bound input remains alive until the prepared statement is finalized.

## API references

- [SQLite statement preparation and execution](https://www.sqlite.org/c3ref/stmt.html)
- [SQLite value binding](https://sqlite.org/c3ref/bind_blob.html)
- [Go SQLite driver](https://github.com/mattn/go-sqlite3)
- [PDO prepared statements](https://www.php.net/manual/en/pdo.prepare.php)
- [Node SQLite API](https://github.com/TryGhost/node-sqlite3/wiki/API)
- [Microsoft.Data.Sqlite 8.0.21](https://www.nuget.org/packages/Microsoft.Data.Sqlite/8.0.21)
