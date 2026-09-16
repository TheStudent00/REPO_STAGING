// probe 12 -- unary !
#[no_mangle]
pub fn op_12(a: i32) -> <i32 as core::ops::Not>::Output {
    !a
}
