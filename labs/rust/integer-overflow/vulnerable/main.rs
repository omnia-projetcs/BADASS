fn main() { let value = std::env::args().nth(1).expect("input");
let n: u32=value.parse().unwrap(); print!("{}", n.wrapping_mul(100));
}
