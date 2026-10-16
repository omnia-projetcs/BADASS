fn main() { let value = std::env::args().nth(1).expect("input");
if value != "welcome.txt" { print!("DENIED"); return; } print!("{}", std::fs::read_to_string("public/welcome.txt").unwrap());
}
