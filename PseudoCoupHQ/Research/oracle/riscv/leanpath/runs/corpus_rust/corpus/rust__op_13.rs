// probe 13 -- unary !
#[no_mangle]
pub fn op_13(a: i64) -> <i64 as core::ops::Not>::Output {
    !a
}
