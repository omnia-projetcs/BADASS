fn main() { let value = std::env::args().nth(1).expect("input");
print!("<p>{}</p>", value);
}
