// probe 495 -- binary <<
#[no_mangle]
pub fn op_495(a: bool, b: f32) -> <bool as core::ops::Shl<f32>>::Output {
    a << b
}
