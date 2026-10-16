fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let decision: Result<bool, &str> = if value == "backend-down" {
        Err("Authorization unavailable")
    } else {
        Ok(value == "authorized")
    };
    Ok(match decision {
        Ok(true) => "ALLOWED",
        Ok(false) => "DENIED",
        Err(_) => "ALLOWED",
    }
    .to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
