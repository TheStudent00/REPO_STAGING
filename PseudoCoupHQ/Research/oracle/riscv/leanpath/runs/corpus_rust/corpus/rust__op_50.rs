// probe 50 -- unary ?
#[no_mangle]
pub fn op_50(a: u64) -> u64 {
    a?
}
