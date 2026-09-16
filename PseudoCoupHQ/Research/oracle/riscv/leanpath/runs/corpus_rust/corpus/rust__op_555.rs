// probe 555 -- binary +
#[no_mangle]
pub fn op_555(a: f32, b: f32) -> <f32 as core::ops::Add<f32>>::Output {
    a + b
}
