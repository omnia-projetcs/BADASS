fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let quantity: i64 = value.parse()?;
    if !(1..=100).contains(&quantity) {
        return Ok("DENIED".to_string());
    }
    Ok((1000 - quantity * 10).to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
