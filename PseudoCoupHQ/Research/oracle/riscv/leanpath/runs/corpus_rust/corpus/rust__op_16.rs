// probe 16 -- unary !
#[no_mangle]
pub fn op_16(a: f64) -> <f64 as core::ops::Not>::Output {
    !a
}
