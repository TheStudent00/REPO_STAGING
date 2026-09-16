// probe 30 -- unary &raw mut
#[no_mangle]
pub fn op_30(a: i32) -> i32 {
    &raw mut a
}
