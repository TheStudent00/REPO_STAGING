// probe 0 -- unary -
#[no_mangle]
pub fn op_0(a: i32) -> <i32 as core::ops::Neg>::Output {
    -a
}
