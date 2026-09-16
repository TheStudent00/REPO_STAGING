// probe 15 -- unary !
#[no_mangle]
pub fn op_15(a: f32) -> <f32 as core::ops::Not>::Output {
    !a
}
