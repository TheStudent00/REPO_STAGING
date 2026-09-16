// probe 609 -- binary *
#[no_mangle]
pub fn op_609(a: i32, b: f32) -> <i32 as core::ops::Mul<f32>>::Output {
    a * b
}
