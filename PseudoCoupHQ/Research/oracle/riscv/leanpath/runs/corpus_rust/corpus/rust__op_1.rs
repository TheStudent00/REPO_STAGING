// probe 1 -- unary -
#[no_mangle]
pub fn op_1(a: i64) -> <i64 as core::ops::Neg>::Output {
    -a
}
