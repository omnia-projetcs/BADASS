use std::ffi::{CStr, CString};
use std::os::raw::{c_char, c_int, c_uchar, c_void};
use std::ptr;

// SQLite's native API keeps this fixture independent of a Cargo download.
// Opaque handles are never dereferenced by Rust; Drop releases them once.
#[link(name = "sqlite3")]
extern "C" {
    fn sqlite3_open(name: *const c_char, db: *mut *mut c_void) -> c_int;
    fn sqlite3_close(db: *mut c_void) -> c_int;
    fn sqlite3_exec(
        db: *mut c_void,
        sql: *const c_char,
        callback: Option<
            unsafe extern "C" fn(*mut c_void, c_int, *mut *mut c_char, *mut *mut c_char) -> c_int,
        >,
        context: *mut c_void,
        error: *mut *mut c_char,
    ) -> c_int;
    fn sqlite3_prepare_v2(
        db: *mut c_void,
        sql: *const c_char,
        size: c_int,
        statement: *mut *mut c_void,
        tail: *mut *const c_char,
    ) -> c_int;
    fn sqlite3_step(statement: *mut c_void) -> c_int;
    fn sqlite3_column_text(statement: *mut c_void, column: c_int) -> *const c_uchar;
    fn sqlite3_finalize(statement: *mut c_void) -> c_int;
}

struct Database(*mut c_void);
impl Drop for Database {
    fn drop(&mut self) {
        unsafe {
            sqlite3_close(self.0);
        }
    }
}
struct Statement(*mut c_void);
impl Drop for Statement {
    fn drop(&mut self) {
        unsafe {
            sqlite3_finalize(self.0);
        }
    }
}
fn check(status: c_int) -> Result<(), Box<dyn std::error::Error>> {
    if status != 0 {
        return Err(format!("SQLite operation failed: {}", status).into());
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // The vulnerable query deliberately interpolates this untrusted value.
    let value = CString::new(std::env::args().nth(1).ok_or("Expected one value")?)?;
    let mut raw_db = ptr::null_mut();
    let status = unsafe { sqlite3_open(b":memory:\0".as_ptr().cast(), &mut raw_db) };
    let db = Database(raw_db);
    check(status)?;
    let setup = CString::new(
        "CREATE TABLE users(name TEXT NOT NULL); INSERT INTO users VALUES ('alice'),('admin');",
    )?;
    check(unsafe { sqlite3_exec(db.0, setup.as_ptr(), None, ptr::null_mut(), ptr::null_mut()) })?;
    let query = CString::new(format!(
        "SELECT name FROM users WHERE name = '{}'",
        value.to_str()?
    ))?;
    let mut raw_statement = ptr::null_mut();
    let status = unsafe {
        sqlite3_prepare_v2(
            db.0,
            query.as_ptr(),
            -1,
            &mut raw_statement,
            ptr::null_mut(),
        )
    };
    let statement = Statement(raw_statement);
    check(status)?;
    loop {
        match unsafe { sqlite3_step(statement.0) } {
            100 => {
                let name = unsafe { sqlite3_column_text(statement.0, 0) };
                if name.is_null() {
                    return Err("Unexpected NULL result".into());
                }
                println!(
                    "{}",
                    unsafe { CStr::from_ptr(name.cast()) }.to_string_lossy()
                );
            }
            101 => break,
            code => return Err(format!("SQLite query failed: {}", code).into()),
        }
    }
    Ok(())
}
