// probe 2 -- unary -
#[no_mangle]
pub fn op_2(a: u64) -> <u64 as core::ops::Neg>::Output {
    -a
}
