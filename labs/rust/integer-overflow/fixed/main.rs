fn main() {
    let value = match std::env::args().nth(1) {
        Some(arg) => arg,
        None => std::process::exit(2),
    };
    match value.parse::<u32>().ok().and_then(|n| n.checked_mul(100)) {
        Some(total) => print!("{}", total),
        None => print!("DENIED"),
    }
}
