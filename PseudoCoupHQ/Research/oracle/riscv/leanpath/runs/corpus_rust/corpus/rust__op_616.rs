// probe 616 -- binary *
#[no_mangle]
pub fn op_616(a: i64, b: f64) -> <i64 as core::ops::Mul<f64>>::Output {
    a * b
}
