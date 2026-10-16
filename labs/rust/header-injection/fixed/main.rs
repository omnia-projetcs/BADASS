fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    if value.contains('\r') || value.contains('\n') {
        return Ok("DENIED".to_string());
    }
    Ok("X-User: ".to_string() + value + "\r\n\r\nBODY")
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
