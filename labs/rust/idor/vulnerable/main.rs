fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let records = [("alice", "ALICE_DATA"), ("bob", "BOB_PRIVATE")];
    let record = records.iter().find(|(owner, _)| *owner == value);
    if let Some((owner, data)) = record {
        let _ = owner;
        return Ok(data.to_string());
    }
    Ok("NOT_FOUND".to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
