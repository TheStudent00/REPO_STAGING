// probe 26 -- unary &raw const
#[no_mangle]
pub fn op_26(a: u64) -> u64 {
    &raw const a
}
