fn constant_time_equals(a: &[u8], b: &[u8]) -> bool {
    let max_len = a.len().max(b.len());
    let mut diff = a.len() ^ b.len();
    for i in 0..max_len {
        let ca = a.get(i).copied().unwrap_or(0);
        let cb = b.get(i).copied().unwrap_or(0);
        diff |= usize::from(ca ^ cb);
    }
    diff == 0
}

fn run(value: &str) -> Result<String, Box<dyn std::error::Error>> {
    let expected = std::env::var("BADASS_ADMIN_PASSWORD").unwrap_or_default();
    Ok(if !expected.is_empty() && constant_time_equals(value.as_bytes(), expected.as_bytes()) {
        "ADMIN"
    } else {
        "DENIED"
    }
    .to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let value = std::env::args().nth(1).ok_or("Expected one input")?;
    print!("{}", run(&value)?);
    Ok(())
}
