// probe 32 -- unary &raw mut
#[no_mangle]
pub fn op_32(a: u64) -> u64 {
    &raw mut a
}
