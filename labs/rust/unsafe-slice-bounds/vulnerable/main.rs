// Rust handler using unsafe get_unchecked on a stack array to read an adjacent secret slot.
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
    if idx < 4 {
        let val = unsafe { *public_slice.get_unchecked(idx) };
        print!("{}", val);
    } else {
        print!("DENIED");
    }
}
