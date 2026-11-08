fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let expected = std::env::var("BADASS_ADMIN_PASSWORD").unwrap_or_default();
    Ok(if !expected.is_empty() && value == expected {
        "ADMIN"
    } else {
        "DENIED"
    }
    .to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
