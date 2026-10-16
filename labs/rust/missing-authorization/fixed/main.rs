fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    if value == "health" {
        return Ok("HEALTHY".to_string());
    }
    let role = "user";
    let _ = role;
    let mut users = vec!["alice", "bob"];
    if role != "admin" {
        return Ok("DENIED".to_string());
    }
    users.clear();
    Ok("USERS_DELETED".to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
