// probe 628 -- binary *
#[no_mangle]
pub fn op_628(a: f32, b: f64) -> <f32 as core::ops::Mul<f64>>::Output {
    a * b
}
