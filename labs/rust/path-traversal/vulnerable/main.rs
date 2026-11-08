fn main() { let value = std::env::args().nth(1).expect("input");
print!("{}", std::fs::read_to_string(format!("public/{}", value)).unwrap());
}
