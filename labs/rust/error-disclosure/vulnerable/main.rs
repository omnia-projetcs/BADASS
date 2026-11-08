fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    if value == "ok" {
        return Ok("OK".to_string());
    }
    match std::fs::read_to_string("missing-database") {
        Ok(_) => Ok("OK".to_string()),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            Ok("db://admin:LAB_SECRET@database/internal".to_string())
        }
        Err(error) => Err(error.into()),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
