// probe 622 -- binary *
#[no_mangle]
pub fn op_622(a: u64, b: f64) -> <u64 as core::ops::Mul<f64>>::Output {
    a * b
}
