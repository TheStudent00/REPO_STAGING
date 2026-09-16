// probe 591 -- binary -
#[no_mangle]
pub fn op_591(a: f32, b: f32) -> <f32 as core::ops::Sub<f32>>::Output {
    a - b
}
