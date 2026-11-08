fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut encoded = String::new();
    for ch in value.chars() {
        encoded.push(ch);
    }
    std::fs::write("audit.log", "user=".to_string() + &encoded)?;
    Ok(std::fs::read_to_string("audit.log")?)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
