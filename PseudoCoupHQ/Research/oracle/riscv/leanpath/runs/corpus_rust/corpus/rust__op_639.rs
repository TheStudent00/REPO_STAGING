// probe 639 -- binary *
#[no_mangle]
pub fn op_639(a: bool, b: f32) -> <bool as core::ops::Mul<f32>>::Output {
    a * b
}
