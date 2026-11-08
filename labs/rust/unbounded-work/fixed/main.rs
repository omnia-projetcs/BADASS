fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let size: usize = value.parse()?;
    if size > 100 {
        return Ok("DENIED".to_string());
    }
    let data = vec![0u8; size];
    Ok(data.len().to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
