// probe 621 -- binary *
#[no_mangle]
pub fn op_621(a: u64, b: f32) -> <u64 as core::ops::Mul<f32>>::Output {
    a * b
}
