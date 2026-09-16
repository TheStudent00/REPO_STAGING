// probe 640 -- binary *
#[no_mangle]
pub fn op_640(a: bool, b: f64) -> <bool as core::ops::Mul<f64>>::Output {
    a * b
}
