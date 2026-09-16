// probe 573 -- binary -
#[no_mangle]
pub fn op_573(a: i32, b: f32) -> <i32 as core::ops::Sub<f32>>::Output {
    a - b
}
