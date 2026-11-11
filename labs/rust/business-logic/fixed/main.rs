fn run(value: &str) -> String {
    if value.starts_with("-0") || value.starts_with('+') {
        return "DENIED".to_string();
    }
    let quantity: i64 = match value.parse() {
        Ok(parsed) => parsed,
        Err(_) => return "DENIED".to_string(),
    };
    if !(1..=100).contains(&quantity) {
        return "DENIED".to_string();
    }
    (1000 - quantity * 10).to_string()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value));
    Ok(())
}
