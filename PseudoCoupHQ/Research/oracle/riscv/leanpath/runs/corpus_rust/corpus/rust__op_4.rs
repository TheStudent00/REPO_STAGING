// probe 4 -- unary -
#[no_mangle]
pub fn op_4(a: f64) -> <f64 as core::ops::Neg>::Output {
    -a
}
