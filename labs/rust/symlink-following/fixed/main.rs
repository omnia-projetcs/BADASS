fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    use std::io::Write;
    if value == "preplaced-link" {
        std::os::unix::fs::symlink("secret.txt", "export.tmp")?;
    }
    let result = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open("export.tmp");
    match result {
        Ok(mut file) => file.write_all(b"LAB_OVERWRITTEN")?,
        Err(error) if error.kind() == std::io::ErrorKind::AlreadyExists => (),
        Err(error) => return Err(error.into()),
    }
    Ok(std::fs::read_to_string("secret.txt")?)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
