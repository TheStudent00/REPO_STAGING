// probe 624 -- binary *
#[no_mangle]
pub fn op_624(a: f32, b: i32) -> <f32 as core::ops::Mul<i32>>::Output {
    a * b
}
