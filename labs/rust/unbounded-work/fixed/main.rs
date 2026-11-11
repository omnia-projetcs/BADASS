fn run(value: &str) -> String {
    if value.starts_with('+') {
        return "DENIED".to_string();
    }
    let size: usize = match value.parse() {
        Ok(parsed) => parsed,
        Err(_) => return "DENIED".to_string(),
    };
    if size > 100 {
        return "DENIED".to_string();
    }
    let data = vec![0u8; size];
    data.len().to_string()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value));
    Ok(())
}
