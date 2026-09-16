// probe 25 -- unary &raw const
#[no_mangle]
pub fn op_25(a: i64) -> i64 {
    &raw const a
}
