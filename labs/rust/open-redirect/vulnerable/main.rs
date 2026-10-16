fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    Ok("Location: ".to_string() + value)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
