// Ground truth: native rustc computing what the transpiled pipeline computes.
// Extended 2026-07-25 with the newly-cut paths: divisor -1 (CheckedDivOrRemSeq
// guard) and the full unsigned udiv/urem family.
fn main() {
    let vals: [i64; 9] = [-7, -3, -2, -1, 0, 1, 2, 3, 7];
    for &a in vals.iter() {
        for &b in vals.iter() {
            let add = a.wrapping_add(b);
            let sub = a.wrapping_sub(b);
            let mul = a.wrapping_mul(b);
            // sdiv still refuses MIN/-1 (genuine overflow trap, not guarded)
            let can_div = b != 0 && !(a == i64::MIN && b == -1);
            // srem now handles b == -1 via the guard
            let can_rem = b != 0;
            print!("{} {} {} {} {}", a, b, add, sub, mul);
            if can_div { print!(" {}", a / b); } else { print!(" -"); }
            if can_rem { print!(" {}", a % b); } else { print!(" -"); }
            println!();
        }
    }
    // unsigned grid
    let uvals: [u64; 7] = [1, 2, 3, 7, 1 << 63, u64::MAX - 1, u64::MAX];
    for &a in uvals.iter() {
        for &b in uvals.iter() {
            println!("u {} {} {} {}", a, b, a / b, a % b);
        }
    }
}
