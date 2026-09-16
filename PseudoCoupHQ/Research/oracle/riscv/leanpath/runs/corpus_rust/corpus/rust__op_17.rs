// probe 17 -- unary !
#[no_mangle]
pub fn op_17(a: bool) -> <bool as core::ops::Not>::Output {
    !a
}
