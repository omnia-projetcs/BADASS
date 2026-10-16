fn main() { let value = std::env::args().nth(1).expect("input");
let n: u32=value.parse().unwrap(); match n.checked_mul(100) {Some(total)=>print!("{}",total),None=>print!("DENIED")}
}
