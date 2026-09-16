// probe 610 -- binary *
#[no_mangle]
pub fn op_610(a: i32, b: f64) -> <i32 as core::ops::Mul<f64>>::Output {
    a * b
}
