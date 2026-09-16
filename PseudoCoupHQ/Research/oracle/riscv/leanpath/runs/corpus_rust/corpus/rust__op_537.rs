// probe 537 -- binary +
#[no_mangle]
pub fn op_537(a: i32, b: f32) -> <i32 as core::ops::Add<f32>>::Output {
    a + b
}
