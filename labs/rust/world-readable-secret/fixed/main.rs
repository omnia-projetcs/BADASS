fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    use std::io::Write;
    use std::os::unix::fs::{OpenOptionsExt, PermissionsExt};
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .mode(0o600)
        .open("stored-secret")?;
    file.write_all(if value == "public" {
        b"PUBLIC"
    } else {
        b"LAB_SECRET"
    })?;
    file.set_permissions(std::fs::Permissions::from_mode(if value == "public" {
        0o644
    } else {
        0o600
    }))?;
    Ok(format!(
        "{:04o}",
        file.metadata()?.permissions().mode() & 0o777
    ))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
