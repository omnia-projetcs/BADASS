// Rust handler replacing unsafe get_unchecked with safe checked slice indexing.
fn main() {
    let arg = match std::env::args().nth(1) {
        Some(v) => v,
        None => std::process::exit(2),
    };
    let idx: usize = match arg.parse() {
        Ok(n) => n,
        Err(_) => {
            print!("DENIED");
            return;
        }
    };
    let memory: [i32; 4] = [10, 20, 30, 9999];
    let public_slice = &memory[..3];
    match public_slice.get(idx) {
        Some(val) => print!("{}", val),
        None => print!("DENIED"),
    }
}
