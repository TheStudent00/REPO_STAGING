// probe 31 -- unary &raw mut
#[no_mangle]
pub fn op_31(a: i64) -> i64 {
    &raw mut a
}
