// probe 3 -- unary -
#[no_mangle]
pub fn op_3(a: f32) -> <f32 as core::ops::Neg>::Output {
    -a
}
