// probe 567 -- binary +
#[no_mangle]
pub fn op_567(a: bool, b: f32) -> <bool as core::ops::Add<f32>>::Output {
    a + b
}
