// probe 14 -- unary !
#[no_mangle]
pub fn op_14(a: u64) -> <u64 as core::ops::Not>::Output {
    !a
}
