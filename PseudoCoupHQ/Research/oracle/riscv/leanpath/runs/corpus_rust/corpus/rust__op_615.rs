// probe 615 -- binary *
#[no_mangle]
pub fn op_615(a: i64, b: f32) -> <i64 as core::ops::Mul<f32>>::Output {
    a * b
}
