// probe 443 -- binary >=
#[no_mangle]
pub fn op_443(a: u64, b: bool) -> bool {
    a >= b
}
