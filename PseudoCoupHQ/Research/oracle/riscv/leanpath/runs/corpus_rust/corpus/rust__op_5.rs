// probe 5 -- unary -
#[no_mangle]
pub fn op_5(a: bool) -> <bool as core::ops::Neg>::Output {
    -a
}
