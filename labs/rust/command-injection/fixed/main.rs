fn main() { let value = std::env::args().nth(1).expect("input");
let out = std::process::Command::new("/usr/bin/printf").args(["%s", &value]).output().unwrap(); print!("{}", String::from_utf8(out.stdout).unwrap());
}
