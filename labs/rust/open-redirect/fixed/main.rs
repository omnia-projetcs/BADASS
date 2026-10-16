fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    if value != "/home" && value != "/profile" {
        return Ok("DENIED".to_string());
    }
    Ok("Location: ".to_string() + value)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
