// probe 166 -- binary &
#[no_mangle]
pub fn op_166(a: f64, b: f64) -> <f64 as core::ops::BitAnd<f64>>::Output {
    a & b
}
