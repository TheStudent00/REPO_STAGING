// Pinned census fixture: representative Rust constructs (the shapes
// the compiler-source ingress meets: match, struct, impl, arithmetic,
// if-let, method calls). Do not edit.
struct Encoder {
    rex: u8,
    wide: bool,
}

impl Encoder {
    fn encode(&self, reg: u8, rm: u8) -> u8 {
        let base: u8 = 0x40;
        let w: u8 = if self.wide { 1 } else { 0 };
        base | (w << 3) | ((reg & 7) >> 1) | (rm & 7)
    }
}

fn route(op: &str, a: i64, b: i64) -> i64 {
    match op {
        "div" => a / b,
        "rem" => a % b,
        _ => a.wrapping_mul(b),
    }
}

fn main() {
    let e = Encoder { rex: 0x40, wide: true };
    if let 0x40..=0x4f = e.rex {
        println!("{} {}", e.encode(3, 5), route("div", -7, 2));
    }
}
